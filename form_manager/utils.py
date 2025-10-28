import datetime as _dt
import decimal
import json

from django import forms

from .models import FormAuditDetail, UserOrganizationMembership


def build_dynamic_form(form_definition, data=None, initial=None, disabled=False):
    fields = {}
    schema_fields = []
    if isinstance(form_definition.schema.get("sections"), list):
        for s in form_definition.schema.get("sections", []):
            schema_fields.extend(s.get("fields", []))
    schema_fields.extend(form_definition.schema.get("fields", []))

    for field in schema_fields:
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
                label=label, required=required, help_text=help_text, max_length=max_length
            )
        elif field_type == "email":
            fields[name] = forms.EmailField(label=label, required=required, help_text=help_text)
        elif field_type == "number":
            fields[name] = forms.DecimalField(
                label=label,
                required=required,
                help_text=help_text,
                min_value=min_value,
                max_value=max_value,
            )
        elif field_type == "radio":
            choices = field.get("choices", [])
            fields[name] = forms.ChoiceField(
                label=label,
                choices=[(c, c) for c in choices],
                widget=forms.RadioSelect,
                required=required,
                help_text=help_text,
            )
        else:
            fields[name] = forms.CharField(label=label, required=required, help_text=help_text)

    FormClass = type("DynamicForm", (forms.Form,), fields)
    form = FormClass(data=data, initial=initial)
    if disabled:
        for f in form.fields.values():
            f.disabled = True
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
