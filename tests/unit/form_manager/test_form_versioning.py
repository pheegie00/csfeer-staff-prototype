import copy

import pytest
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.utils import timezone
from organizations.models import OrganizationProfile

from form_manager.constants import CSBGAnnualReportForms, FormFamilies
from form_manager.models import FormDefinition, FormEntry


def _make_definition(variant: str, *, name=None, family=None, schema=None) -> FormDefinition:
    return FormDefinition.objects.create(
        family=family or FormFamilies.CSBG_ANNUAL_REPORT,
        name=name or CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0,
        variant=variant,
        schema=schema if schema is not None else {"version": variant, "fields": ["a"]},
        schema_class="TestSchema",
    )


@pytest.mark.django_db
def test_multiple_variants_of_same_form_coexist():
    """AC1: the data model supports multiple versions per form template."""
    v1 = _make_definition("1.0.0")
    v2 = _make_definition("2.0.0")
    v3 = _make_definition("2.1.0")

    rows = FormDefinition.objects.filter(name=v1.name).order_by("variant")
    assert list(rows.values_list("variant", flat=True)) == ["1.0.0", "2.0.0", "2.1.0"]
    assert {v1.pk, v2.pk, v3.pk} == set(rows.values_list("pk", flat=True))


@pytest.mark.django_db
def test_form_definition_unique_constraint_on_name_and_variant():
    """AC1 guardrail: (name, variant) is unique; duplicates raise IntegrityError."""
    _make_definition("1.0.0")
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            _make_definition("1.0.0")


@pytest.mark.django_db
def test_form_entry_is_permanently_linked_to_its_template_version(create_user):
    """AC2: a submission keeps pointing to the exact FormDefinition it was created against."""
    user = create_user
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    v1 = _make_definition("1.0.0")
    entry = FormEntry.objects.create(
        form_definition=v1, organization=org, created_by=user, version_number=1
    )

    # Publish a new template version. The submission must still point at v1.
    _make_definition("2.0.0")

    entry.refresh_from_db()
    assert entry.form_definition_id == v1.pk  # type: ignore[attr-defined]
    assert entry.form_definition.variant == "1.0.0"


@pytest.mark.django_db
def test_form_definition_with_entries_cannot_be_deleted(create_user):
    """AC2 guardrail: PROTECT prevents losing the template a submission was filed against."""
    user = create_user
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    v1 = _make_definition("1.0.0")
    FormEntry.objects.create(
        form_definition=v1, organization=org, created_by=user, version_number=1
    )

    with pytest.raises(ProtectedError):
        v1.delete()

    assert FormDefinition.objects.filter(pk=v1.pk).exists()


@pytest.mark.django_db
def test_publishing_new_version_does_not_mutate_prior_version(create_user):
    """AC3: publishing v2 leaves v1's row (schema, schema_class, is_active) untouched."""
    v1 = _make_definition("1.0.0", schema={"version": "1.0.0", "fields": ["a", "b"]})
    snapshot = {
        "family": v1.family,
        "name": v1.name,
        "variant": v1.variant,
        "schema": copy.deepcopy(v1.schema),
        "schema_class": v1.schema_class,
        "is_active": v1.is_active,
    }

    _make_definition("2.0.0", schema={"version": "2.0.0", "fields": ["a", "b", "c"]})

    v1.refresh_from_db()
    assert v1.family == snapshot["family"]
    assert v1.name == snapshot["name"]
    assert v1.variant == snapshot["variant"]
    assert v1.schema == snapshot["schema"]
    assert v1.schema_class == snapshot["schema_class"]
    assert v1.is_active == snapshot["is_active"]


@pytest.mark.django_db
def test_prior_version_submissions_remain_intact_and_queryable(create_user):
    """AC4: after a new version publishes, old submissions are unchanged and findable."""
    user = create_user
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    v1 = _make_definition("1.0.0")
    entry = FormEntry.objects.create(
        form_definition=v1,
        organization=org,
        created_by=user,
        version_number=1,
        data={"first_name": "Ada", "last_name": "Lovelace"},
        status="submitted",
        submitted_at=timezone.now(),
    )
    original_updated_at = entry.updated_at

    # Publish two more versions of the same template.
    _make_definition("2.0.0")
    _make_definition("2.1.0")

    entry.refresh_from_db()
    assert entry.data == {"first_name": "Ada", "last_name": "Lovelace"}
    assert entry.status == "submitted"
    assert entry.updated_at == original_updated_at

    # Queryable by the historical variant.
    by_variant = FormEntry.objects.filter(form_definition__variant="1.0.0")
    assert list(by_variant.values_list("pk", flat=True)) == [entry.pk]

    # And the new versions have no submissions yet.
    assert not FormEntry.objects.filter(form_definition__variant="2.0.0").exists()
    assert not FormEntry.objects.filter(form_definition__variant="2.1.0").exists()
