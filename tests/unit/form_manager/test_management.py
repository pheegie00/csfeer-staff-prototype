import copy
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.utils import timezone
from organizations.models import OrganizationProfile

from form_manager.models import FormDefinition, FormEntry
from form_manager.schema.forms import ALL_FORM_SCHEMAS
from form_manager.utils import get_form_definitions
from tests.unit.form_manager.fixtures.use_test_schema import TestSchema, TestSchema_3_1

MODULE_PATH = "form_manager.management.commands.load_initial_forms"


@pytest.mark.django_db
def test_correctly_loads_form_schemas_in_db(django_db_setup):
    """Ensure the load_initial_forms command loads successfully."""

    call_command("load_initial_forms")

    assert FormDefinition.objects.count() == len(
        ALL_FORM_SCHEMAS
    ), "Failed to load all form schemas"

    for schema in get_form_definitions():

        schema_instance = schema.model_construct()

        form_definition_qs = FormDefinition.objects.filter(
            family=schema_instance.family,
            name=schema_instance.name,
            variant=schema_instance.variant,
        )

        assert form_definition_qs.count() == 1, f"Failed to load {schema_instance.name} schema"

        form_definition = form_definition_qs.first()

        assert form_definition.schema_class == schema.__name__  # type: ignore

        assert form_definition and (
            form_definition.schema == schema.model_json_schema()
        ), f"{schema.__name__} schema differs in db"


@pytest.mark.django_db
def test_load_initial_forms_is_idempotent(empty_form_definitions, use_test_schema):
    """Re-running the publish command without --force is a no-op for known versions."""
    call_command("load_initial_forms")
    first_count = FormDefinition.objects.count()
    assert first_count == 1
    original = FormDefinition.objects.get()
    original_updated_at = original.updated_at

    call_command("load_initial_forms")

    assert FormDefinition.objects.count() == first_count
    refreshed = FormDefinition.objects.get(pk=original.pk)
    assert refreshed.updated_at == original_updated_at


@pytest.mark.django_db
def test_load_initial_forms_force_resyncs_schema(empty_form_definitions, use_test_schema):
    """--force restores all canonical defaults (schema, schema_class, family, is_active)
    when the DB row has drifted."""
    call_command("load_initial_forms")
    definition = FormDefinition.objects.get()
    canonical_schema = use_test_schema.model_json_schema()
    assert definition.schema == canonical_schema

    definition.schema = {"tampered": True}
    definition.schema_class = "Tampered"
    definition.family = "tampered_family"
    definition.is_active = False
    definition.save(update_fields=["schema", "schema_class", "family", "is_active"])

    call_command("load_initial_forms", "--force")

    definition.refresh_from_db()
    assert definition.schema == canonical_schema
    assert definition.schema_class == use_test_schema.__name__
    family_prop = canonical_schema["properties"]["family"]
    assert definition.family == (family_prop.get("const") or family_prop.get("default"))
    assert definition.is_active is True


@pytest.mark.django_db
def test_load_initial_forms_force_preserves_existing_submissions(
    empty_form_definitions, use_test_schema, create_user
):
    """Re-publishing with --force must not disturb submissions linked to the template."""
    user = create_user
    call_command("load_initial_forms")
    definition = FormDefinition.objects.get()
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    entry = FormEntry.objects.create(
        form_definition=definition,
        organization=org,
        created_by=user,
        version_number=1,
        data={"first_name": "Grace", "last_name": "Hopper"},
        status="submitted",
        submitted_at=timezone.now(),
    )
    original_entry_updated_at = entry.updated_at

    call_command("load_initial_forms", "--force")

    entry.refresh_from_db()
    assert entry.form_definition.pk == definition.pk
    assert entry.data == {"first_name": "Grace", "last_name": "Hopper"}
    assert entry.status == "submitted"
    assert entry.updated_at == original_entry_updated_at


@pytest.mark.django_db
def test_publishing_new_variant_via_command_preserves_prior_version_and_entries(
    empty_form_definitions, create_user
):
    """End-to-end: publish v3.0, then re-run the command with v3.0 + v3.1 in the
    registry. The new version lands as a sibling row; the old row and any
    submissions filed against it are untouched. Mirrors the real-world release
    flow exercised by TribalShortForm_3_1.
    """
    user = create_user
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    with patch(f"{MODULE_PATH}.get_form_definitions", return_value=[TestSchema]):
        call_command("load_initial_forms")

    v1 = FormDefinition.objects.get()
    entry = FormEntry.objects.create(
        form_definition=v1,
        organization=org,
        created_by=user,
        version_number=1,
        data={"first_name": "Ada"},
        status="submitted",
        submitted_at=timezone.now(),
    )
    snapshot = copy.deepcopy(v1.schema)
    original_v1_updated_at = v1.updated_at

    with patch(f"{MODULE_PATH}.get_form_definitions", return_value=[TestSchema, TestSchema_3_1]):
        call_command("load_initial_forms")

    versions = FormDefinition.objects.filter(name=v1.name).order_by("variant")
    assert list(versions.values_list("variant", flat=True)) == ["3.0.4", "3.1.0"]

    v1.refresh_from_db()
    assert v1.schema == snapshot
    assert v1.updated_at == original_v1_updated_at

    entry.refresh_from_db()
    assert entry.form_definition.pk == v1.pk
    assert entry.data == {"first_name": "Ada"}
    assert entry.status == "submitted"
