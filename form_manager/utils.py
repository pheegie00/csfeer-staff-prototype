import datetime as _dt
import decimal
import json
import logging
from inspect import isclass

from .models import FormAuditDetail, UserOrganizationMembership
from .rendering.pydantic_form import PydanticJSONSchemaForm
from .schema import forms as form_schemas

logger = logging.getLogger(__name__)


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
    FormClass = type("DynamicForm", (PydanticJSONSchemaForm,), {"_schema": form_definition.schema})

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


def get_form_definitions() -> list[form_schemas.BaseFormSchema]:
    """Returns a list of form definition classes"""

    ret = []

    for attr_name in form_schemas.__dir__():  # type: ignore

        form_class = getattr(form_schemas, attr_name)

        if (
            isclass(form_class)
            and issubclass(form_class, form_schemas.BaseFormSchema)
            and form_class != form_schemas.BaseFormSchema
        ):
            ret.append(form_class)

    return ret
