import datetime as _dt
import decimal
import json
import logging
from inspect import isclass

from django.forms import Form

from form_manager.models import (
    FormAuditDetail,
    FormAuditTrail,
    FormEntry,
    UserOrganizationMembership,
)
from form_manager.schema import forms as form_schemas

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


def save_form_entry(form_class: type[Form], form_entry: FormEntry, request):
    old_data = form_entry.data.copy() if form_entry.data else {}

    # Construct a form instance with POST vars and an initial empty dict in order to
    # get normalized data from the form. The empty initial dict is important, because
    # if we passed in the db data values as initial data, the form would indicate that
    # all of the fields that aren't being passed in via POST vars have changed, and
    # that's not what we want for this purpose.
    form = form_class(request.POST, initial={})

    new_data = {}

    logger.info("Found the following changed fields: %s", form.changed_data)

    # construct a dict of changed data values
    for field_name in form.changed_data:
        new_data[field_name] = form[field_name].value()

    # merge the old and new data
    final_data = old_data | new_data

    form_entry.data = final_data
    FormAuditTrail.objects.create(form_entry=form_entry, user=request.user, action="submit")
    record_field_diffs(form_entry, old_data, form_entry.data, user=request.user)

    form_entry.save()

    logger.info(
        "FormEntry %s saved by user %s. Data: %s",
        form_entry.pk,
        request.user.pk,
        form_entry.data,
    )
