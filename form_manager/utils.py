import datetime as _dt
import decimal
import json
import logging
import os
import uuid
from inspect import isclass

from django import forms
from django.core.files.storage import default_storage
from django.forms import Form

from form_manager.models import (
    FormAuditDetail,
    FormAuditTrail,
    FormEntry,
    UserOrganizationMembership,
)
from form_manager.schema import forms as form_schemas
from form_manager.schema.fields import (
    ACFCalculatedFieldMixin,
    ACFYesNoDisplayField,
)

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
    """Reconstruct form entry state from audit details up to a given moment (created_at cutoff)."""
    qs = FormAuditDetail.objects.filter(form_entry=entry)
    if upto is not None:
        qs = qs.filter(created_at__lte=upto)
    qs = qs.order_by("created_at", "id")
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
        old_s = json.dumps(old, sort_keys=True) if isinstance(old, dict | list) else str(old)
        new_s = json.dumps(new, sort_keys=True) if isinstance(new, dict | list) else str(new)
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
    if isinstance(value, _dt.datetime | _dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
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


def get_fields_to_save(form, request):
    """
    Determine which fields should be saved from POST data.

    Returns fields that:
    - Are valid form fields
    - Have data submitted in POST (including empty values)
    - Are NOT calculated fields (auto-generated)

    Note: Uses Django's widget API to detect submitted data, which
    correctly handles MultiValueField (like ACFYesNoDisplayField) that
    uses multiple POST keys for a single field.
    """
    fields_to_save = []

    for field_name, field in form.fields.items():
        # Skip calculated fields (disabled, auto-generated)
        if isinstance(field, ACFCalculatedFieldMixin):
            continue

        # Use Django's widget API to check if field has data in POST
        # This works for all field types including MultiValueField
        value = field.widget.value_from_datadict(
            request.POST, request.FILES, form.add_prefix(field_name)
        )

        logger.info("Evaluating %s with value %s", field_name, value)

        # If widget found data (even empty string), include this field
        # value_from_datadict returns None if field not in POST
        if isinstance(field, ACFYesNoDisplayField):
            if value and any(value):
                fields_to_save.append(field_name)

        elif value is not None:

            if isinstance(value, list):
                if any(value):
                    logger.info("Adding %s to fields_to_save", field_name)
                    fields_to_save.append(field_name)
            else:
                fields_to_save.append(field_name)

    return fields_to_save


def _persist_uploaded_file(uploaded_file, form_entry: FormEntry, field_name: str) -> str:
    """Persist an uploaded file and return its storage path."""
    file_name = os.path.basename(getattr(uploaded_file, "name", "upload.bin"))
    unique_prefix = uuid.uuid4().hex
    path = f"form_uploads/{form_entry.pk}/{field_name}/{unique_prefix}_{file_name}"
    return default_storage.save(path, uploaded_file)


def save_form_entry(form_class: type[Form], form_entry: FormEntry, request):
    old_data = form_entry.data.copy() if form_entry.data else {}

    # Construct a form instance with POST vars and an initial empty dict in order to
    # get normalized data from the form. The empty initial dict is important, because
    # if we passed in the db data values as initial data, the form would indicate that
    # all of the fields that aren't being passed in via POST vars have changed, and
    # that's not what we want for this purpose.
    form = form_class(request.POST, request.FILES, initial={})

    new_data = {}

    fields_to_save = get_fields_to_save(form, request)
    logger.info("Saving the following fields: %s", fields_to_save)

    # construct a dict of changed data values
    for field_name in fields_to_save:
        field = form.fields[field_name]

        if isinstance(field, forms.FileField):
            prefixed_name = form.add_prefix(field_name)

            # Normalise existing value to a list (handles legacy single-string format)
            current = old_data.get(field_name) or []
            if isinstance(current, str):
                current = [current] if current else []

            # Paths checked for removal via the per-file Remove checkboxes
            to_delete = set(
                getattr(request.POST, "getlist", lambda _: [])(f"{prefixed_name}_delete")
            )

            # Keep files not marked for deletion, then append any new uploads
            remaining = [f for f in current if f not in to_delete]
            if hasattr(request.FILES, "getlist"):
                uploaded_files = request.FILES.getlist(prefixed_name)
            else:
                f = request.FILES.get(prefixed_name)
                uploaded_files = [f] if f is not None else []
            for uploaded_file in uploaded_files:
                remaining.append(_persist_uploaded_file(uploaded_file, form_entry, field_name))

            new_data[field_name] = remaining if remaining else None
            continue

        new_data[field_name] = to_jsonable(form[field_name].value())

    logger.info("Old data: %s", old_data)

    logger.info("New data: %s", new_data)

    # merge the old and new data
    final_data = old_data | new_data

    if final_data == old_data:
        logger.info(
            "Skipping save for FormEntry %s by user %s because no form data changed.",
            form_entry.pk,
            request.user.pk,
        )
        return

    form_entry.data = final_data
    form_entry.save()
    FormAuditTrail.objects.create(form_entry=form_entry, user=request.user, action="save")
    record_field_diffs(form_entry, old_data, form_entry.data, user=request.user)

    logger.info(
        "FormEntry %s saved by user %s. Data: %s",
        form_entry.pk,
        request.user.pk,
        form_entry.data,
    )
