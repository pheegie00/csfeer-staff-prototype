import datetime as _dt
import decimal
import json

from django import forms

from .models import FormAuditDetail, UserOrganizationMembership


def normalize_choices(choices):
    """Normalize choice format to Django's (value, label) tuples."""
    normalized = []
    for choice in choices:
        if isinstance(choice, list) and len(choice) == 2:
            # [value, label] format
            normalized.append(tuple(choice))
        elif isinstance(choice, str):
            # Simple string, use same for value and label
            normalized.append((choice, choice))
        else:
            normalized.append((choice, choice))
    return normalized


def try_parse_json(value: str):
    """Try to parse a string as JSON, return original value on failure."""
    try:
        return json.loads(value)
    except Exception:
        return value


def reconstruct_state(entry, upto=None):
    """Reconstruct form entry state from audit details up to a given timestamp."""
    qs = FormAuditDetail.objects.filter(form_entry=entry)
    if upto is not None:
        qs = qs.filter(timestamp__lte=upto)
    qs = qs.order_by("timestamp", "id")
    state = {}
    for d in qs:
        state[d.field_name] = try_parse_json(d.new_value)
    return state


def build_dynamic_form(form_definition, data=None, initial=None, disabled=False):
    fields = {}
    sections = []

    # Build sections metadata
    if isinstance(form_definition.schema.get("sections"), list):
        for section in form_definition.schema.get("sections", []):
            section_fields = []
            for field in section.get("fields", []):
                section_fields.append(field["name"])
                # Build the field
                name = field["name"]
                label = field.get("label", name)
                required = field.get("required", False)
                help_text = field.get("help_text", "")
                field_type = field.get("type", "text")
                max_length = field.get("max_length")
                min_value = field.get("min")
                max_value = field.get("max")

                if field_type == "text":
                    fields[name] = forms.CharField(
                        label=label,
                        required=required,
                        help_text=help_text,
                        max_length=max_length,
                        widget=forms.TextInput(attrs={"class": "usa-input"}),
                    )
                elif field_type == "email":
                    fields[name] = forms.EmailField(
                        label=label,
                        required=required,
                        help_text=help_text,
                        widget=forms.EmailInput(attrs={"class": "usa-input", "type": "email"}),
                    )
                elif field_type == "number":
                    fields[name] = forms.DecimalField(
                        label=label,
                        required=required,
                        help_text=help_text,
                        min_value=min_value,
                        max_value=max_value,
                        widget=forms.NumberInput(attrs={"class": "usa-input"}),
                    )
                elif field_type == "radio":
                    choices = field.get("choices", [])
                    choices = normalize_choices(choices)
                    widget = forms.RadioSelect(attrs={"class": "usa-radio__input"})
                    widget.template_name = "widgets/uswds_radio.html"
                    widget.option_template_name = "widgets/uswds_radio_option.html"
                    fields[name] = forms.ChoiceField(
                        label=label,
                        choices=choices,
                        widget=widget,
                        required=required,
                        help_text=help_text,
                    )
                elif field_type == "select":
                    choices = field.get("choices", [])
                    choices = normalize_choices(choices)
                    fields[name] = forms.ChoiceField(
                        label=label,
                        choices=choices,
                        widget=forms.Select(attrs={"class": "usa-select"}),
                        required=required,
                        help_text=help_text,
                    )
                elif field_type == "textarea":
                    fields[name] = forms.CharField(
                        label=label,
                        required=required,
                        help_text=help_text,
                        widget=forms.Textarea(attrs={"class": "usa-textarea"}),
                    )
                elif field_type == "date":
                    widget = forms.DateInput(
                        attrs={
                            "class": "usa-input",
                            "aria-describedby": f"{name}-hint" if help_text else None,
                        }
                    )
                    widget.template_name = "widgets/uswds_date.html"
                    fields[name] = forms.DateField(
                        label=label,
                        required=required,
                        help_text=help_text or "mm/dd/yyyy",
                        widget=widget,
                        input_formats=["%m/%d/%Y", "%Y-%m-%d"],
                    )
                else:
                    fields[name] = forms.CharField(
                        label=label,
                        required=required,
                        help_text=help_text,
                        widget=forms.TextInput(attrs={"class": "usa-input"}),
                    )

            sections.append(
                {
                    "title": section.get("title"),
                    "description": section.get("description"),
                    "instructional_note": section.get("instructional_note"),
                    "fields": section_fields,
                }
            )

    FormClass = type("DynamicForm", (forms.Form,), fields)
    form = FormClass(data=data, initial=initial)
    if disabled:
        for f in form.fields.values():
            f.disabled = True

    # Attach sections metadata to form
    setattr(form, "sections", sections)
    return form


def get_user_role(user, organization):
    m = UserOrganizationMembership.objects.filter(user=user, organization=organization).first()
    return m.role if m else None


def user_can_edit(user, organization):
    role = get_user_role(user, organization)
    return role in ["admin", "editor"]


def user_can_submit(user, organization):
    role = get_user_role(user, organization)
    return role in ["admin", "editor"]


def user_can_view(user, organization):
    role = get_user_role(user, organization)
    return role in ["admin", "editor", "viewer"]


def record_field_diffs(form_entry, old_data, new_data, user=None):
    all_keys = set((old_data or {}).keys()) | set((new_data or {}).keys())
    details = []
    for k in all_keys:
        old = old_data.get(k, "") if old_data else ""
        new = new_data.get(k, "") if new_data else ""
        old_s = json.dumps(old, sort_keys=True) if isinstance(old, (dict, list)) else str(old)
        new_s = json.dumps(new, sort_keys=True) if isinstance(new, (dict, list)) else str(new)
        if old_s != new_s:
            details.append(
                FormAuditDetail(
                    form_entry=form_entry, user=user, field_name=k, old_value=old_s, new_value=new_s
                )
            )
    if details:
        FormAuditDetail.objects.bulk_create(details)


def to_jsonable(value):
    """Recursively convert values to JSON-serializable types.
    - Decimal -> float
    - date/datetime -> ISO string
    - dict/list/tuple -> recurse
    """
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (_dt.datetime, _dt.date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value
