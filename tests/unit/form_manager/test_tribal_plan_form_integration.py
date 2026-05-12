"""Integration and unit tests for TribalPlanForm."""

from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.constants import CSBGTribalPlanApplicationForms
from organizations.models import OrganizationProfile
from form_manager.models import FormDefinition, FormEntry
from form_manager.schema.forms.tribal_plan import TribalPlanFormFields
from form_manager.schema.navigation import build_form_edit_url

if TYPE_CHECKING:
    from django.test.client import Client
    from users.models import CoreUser


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tribal_plan_form_schema(django_db_setup):
    """Ensure TribalPlanForm schema is loaded and return its FormDefinition."""
    call_command("load_initial_forms")
    return FormDefinition.objects.get(name=CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN)


@pytest.fixture
def tribal_plan_form_entry(create_user, tribal_plan_form_schema) -> FormEntry:
    """Create a TribalPlanForm entry for testing."""
    user = create_user

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()
    return FormEntry.objects.create(
        form_definition=tribal_plan_form_schema,
        organization=org,
        created_by=user,
        version_number="1",
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_form_data(**overrides) -> dict:
    """Return a complete, valid POST data dict for TribalPlanFormFields.

    All required fields are filled. Override specific keys to test validation
    edge cases.
    """
    data = {
        # Section 1 — Plan Coverage
        "plan_coverage": "one_year",
        "fiscal_year_y1": "fy_2026",
        "fiscal_year_y2": "",
        # Section 1 — Tribal Organization
        "tribal_lead_agency_name": "Test Tribal Lead Agency",
        "org_name": "Test Tribal Nation",
        "is_multi_tribe": "no",
        "multi_tribe_names": "",
        # Section 1 — Authorized Tribal Official
        "authorized_official_name": "John Doe",
        "authorized_official_title": "President",
        "authorized_official_street": "123 Main St",
        "authorized_official_city": "Washington",
        "authorized_official_state": "DC",
        "authorized_official_zip": "20001",
        "authorized_official_phone": "5550001234",
        "authorized_official_extension": "",
        "authorized_official_fax": "",
        "authorized_official_email": "official@tribe.gov",
        "authorized_official_website": "",
        # Section 1 — Point of Contact
        "contact_name": "Jane Smith",
        "contact_title": "CSBG Point of Contact",
        "contact_street": "456 Oak Ave",
        "contact_city": "Washington",
        "contact_state": "DC",
        "contact_zip": "20002",
        "contact_phone": "5550005678",
        "contact_extension": "",
        "contact_fax": "",
        "contact_email": "contact@tribe.gov",
        # Section 1 — Delegation
        "has_delegation": "no",
        "delegation_name": "",
        "delegation_title": "",
        "delegation_phone": "",
        "delegation_extension": "",
        "delegation_email": "",
        # Section 2 — Recognition
        "has_recognition": "yes",
        "recognition_provision_method": "manual",
        "recognition_citation": "Federal Recognition, 25 U.S.C. § 450",
        # Section 3
        "goals_and_objectives": "Improve community well-being through targeted CSBG programs.",
        # Section 4 — YesNoDisplayField submits as _0 / _1 sub-inputs
        "community_feedback_0": "no",
        "community_feedback_1": "",
        # Section 5 — Year 1 Allocations (sum = 100%)
        "alloc_admin_y1": "10.00",
        "alloc_employment_y1": "10.00",
        "alloc_education_y1": "10.00",
        "alloc_income_y1": "10.00",
        "alloc_housing_y1": "10.00",
        "alloc_health_y1": "10.00",
        "alloc_civic_y1": "10.00",
        "alloc_transportation_y1": "10.00",
        "alloc_partnerships_y1": "20.00",
        # Section 5 — Fiscal Controls
        "use_of_funds_acknowledgment": True,
        "has_completed_single_audit": "no",
        "audit_date": "",
        "audit_period_start": "",
        "audit_period_end": "",
        # Section 6
        "individual_eligibility": "Eligibility is determined by income guidelines.",
        "targeted_community_eligibility": "Services target low-income tribal members.",
        # Section 7
        "assurance_narrative": "This narrative describes how programmatic assurances are met.",
        "assurance_attestation": True,
        "assurance_signature": "John Doe",
        # Section 8
        "lobbying_attestation": True,
        "lobbying_signature": "John Doe",
        "drug_free_attestation": True,
        "drug_free_place_of_performance": "123 Main St, Washington DC 20001",
        "drug_free_unidentified_workplaces_0": "no",
        "drug_free_unidentified_workplaces_1": "",
        "drug_free_signature": "John Doe",
        "debarment_attestation": True,
        "debarment_signature": "John Doe",
        "tobacco_attestation": True,
        "tobacco_signature": "John Doe",
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# Integration tests — form loading and rendering
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_tribal_plan_form_schema_loads(django_db_setup, tribal_plan_form_schema):
    """load_initial_forms creates a FormDefinition for TribalPlanForm."""
    assert tribal_plan_form_schema is not None
    assert tribal_plan_form_schema.name == CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN
    assert tribal_plan_form_schema.schema_class == "TribalPlanForm"
    assert tribal_plan_form_schema.is_active


@pytest.mark.django_db
def test_can_start_tribal_plan_form(
    django_db_setup, create_user, tribal_plan_form_schema, authenticated_client_with_user
):
    """Starting a new TribalPlanForm creates a FormEntry and redirects to edit."""
    client, user = authenticated_client_with_user

    url = reverse("form_start", args=[tribal_plan_form_schema.pk])
    response = client.get(url)

    assert response.status_code == 302
    assert FormEntry.objects.count() == 1

    entry = FormEntry.objects.first()
    assert entry and entry.form_definition == tribal_plan_form_schema
    assert entry and response.headers.get("Location", "") == reverse("form_edit", args=[entry.pk])


@pytest.mark.django_db
def test_tribal_plan_form_renders(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """GET on the form edit URL returns 200."""
    url = build_form_edit_url(tribal_plan_form_entry.pk, step_number=0, page_number=0)
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_tribal_plan_form_section1_plan_coverage_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 0, page 0 renders the plan coverage fields."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 0, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "plan_coverage" in content or "Plan Coverage" in content
    assert "fiscal_year_y1" in content or "Fiscal Year" in content


@pytest.mark.django_db
def test_tribal_plan_form_section1_tribal_org_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 0, page 1 renders tribal organization fields including multi-tribe."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 0, "page": 1})

    assert response.status_code == 200
    content = response.content.decode()
    assert "org_name" in content or "Name of Tribe" in content
    assert "is_multi_tribe" in content or "representing more than one Tribe" in content
    assert "tribal_resolution_upload" in content or "Tribal Resolution" in content


@pytest.mark.django_db
def test_tribal_plan_form_section1_authorized_official_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 0, page 2 renders the Authorized Tribal Official fields."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 0, "page": 2})

    assert response.status_code == 200
    content = response.content.decode()
    assert "authorized_official_name" in content or "Authorized Tribal Official" in content
    assert "authorized_official_email" in content or "Email address" in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_y1_allocations_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 4, page 0 renders Year 1 allocation fields when a plan is selected.

    The Y1 card uses server-side conditional rendering on `plan_coverage`, so the
    entry must have a plan selected for the card (and its fields) to render.
    """
    tribal_plan_form_entry.data = {"plan_coverage": "one_year"}
    tribal_plan_form_entry.save(update_fields=["data"])

    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "alloc_admin_y1" in content
    assert "alloc_total_y1" in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_hides_y1_card_without_plan_coverage(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """When no plan has been selected, neither allocation card renders."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "alloc_admin_y1" not in content
    assert "alloc_admin_y2" not in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_two_year_renders_both_cards(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """A two-year plan renders both the Y1 and Y2 allocation cards."""
    tribal_plan_form_entry.data = {"plan_coverage": "two_year"}
    tribal_plan_form_entry.save(update_fields=["data"])

    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "alloc_admin_y1" in content
    assert "alloc_admin_y2" in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_one_year_hides_y2_card(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """A one-year plan renders the Y1 card but not the Y2 card."""
    tribal_plan_form_entry.data = {"plan_coverage": "one_year"}
    tribal_plan_form_entry.save(update_fields=["data"])

    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "alloc_admin_y1" in content
    assert "alloc_admin_y2" not in content


@pytest.mark.django_db
def test_tribal_plan_form_section8_certifications_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 7, page 0 renders the Lobbying Certification."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 7, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "lobbying_attestation" in content or "Lobbying" in content
    assert "lobbying_signature" in content or "Signature" in content


@pytest.mark.django_db
def test_tribal_plan_form_has_eight_steps(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """The form schema has exactly 8 steps."""
    from form_manager.schema.forms.tribal_plan import TribalPlanForm

    schema = TribalPlanForm.model_construct()
    assert len(schema.ui) == 8


# ---------------------------------------------------------------------------
# Unit tests — TribalPlanFormFields.clean() validation
# ---------------------------------------------------------------------------


def test_valid_form_passes():
    """A fully filled one-year plan form passes validation."""
    form = TribalPlanFormFields(data=_valid_form_data())
    assert form.is_valid(), form.errors


def test_y1_allocation_total_must_equal_100():
    """Year 1 allocation fields that sum to less than 100 fail validation."""
    data = _valid_form_data(alloc_partnerships_y1="10.00")  # total = 90
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    error_text = str(form.errors)
    assert "100%" in error_text or "100" in error_text


def test_y1_allocation_total_over_100_fails():
    """Year 1 allocation fields that sum to more than 100 fail validation."""
    data = _valid_form_data(alloc_partnerships_y1="30.00")  # total = 110
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()


def test_multi_tribe_names_required_when_yes():
    """multi_tribe_names is required when is_multi_tribe = yes."""
    data = _valid_form_data(is_multi_tribe="yes", multi_tribe_names="")
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "multi_tribe_names" in form.errors


def test_multi_tribe_names_not_required_when_no():
    """multi_tribe_names is not required when is_multi_tribe = no."""
    data = _valid_form_data(is_multi_tribe="no", multi_tribe_names="")
    form = TribalPlanFormFields(data=data)
    assert form.is_valid(), form.errors


def test_multi_tribe_upload_can_use_existing_saved_file():
    """Existing saved tribal resolution should satisfy conditional upload requirement."""
    data = _valid_form_data(
        is_multi_tribe="yes",
        multi_tribe_names="Tribe A; Tribe B",
        tribal_resolution_upload="",
    )
    form = TribalPlanFormFields(
        data=data, initial={"tribal_resolution_upload": "form_uploads/entry/tribal_resolution.pdf"}
    )
    assert form.is_valid(), form.errors


def test_delegation_fields_required_when_yes():
    """Delegation sub-fields are required when has_delegation = yes."""
    data = _valid_form_data(
        has_delegation="yes",
        delegation_name="",
        delegation_title="",
        delegation_phone="",
        delegation_email="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "delegation_name" in form.errors
    assert "delegation_title" in form.errors
    assert "delegation_phone" in form.errors
    assert "delegation_email" in form.errors


def test_delegation_fields_not_required_when_no():
    """Delegation sub-fields are not required when has_delegation = no."""
    data = _valid_form_data(has_delegation="no")
    form = TribalPlanFormFields(data=data)
    assert form.is_valid(), form.errors


def test_recognition_provision_method_required_when_yes():
    """A provision method is required when has_recognition = yes."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_provision_method="",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_provision_method" in form.errors


def test_recognition_citation_required_when_manual():
    """Citation is required when provision method = manual."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_provision_method="manual",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_citation" in form.errors


def test_recognition_upload_required_when_upload():
    """Upload is required when provision method = upload."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_provision_method="upload",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_upload" in form.errors


def test_recognition_not_required_when_no():
    """No recognition fields are required when has_recognition = no."""
    data = _valid_form_data(
        has_recognition="no",
        recognition_provision_method="",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert form.is_valid(), form.errors


def test_recognition_upload_can_use_existing_saved_file():
    """Existing saved recognition upload satisfies the upload provision method."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_provision_method="upload",
        recognition_citation="",
        recognition_upload="",
    )
    form = TribalPlanFormFields(
        data=data, initial={"recognition_upload": "form_uploads/entry/recognition.pdf"}
    )
    assert form.is_valid(), form.errors


def test_two_year_plan_y2_total_must_equal_100():
    """Year 2 allocation total must be 100% when plan_coverage = two_year."""
    data = _valid_form_data(
        plan_coverage="two_year",
        fiscal_year_y2="fy_2027",
        alloc_admin_y2="10.00",
        alloc_employment_y2="10.00",
        alloc_education_y2="10.00",
        alloc_income_y2="10.00",
        alloc_housing_y2="10.00",
        alloc_health_y2="10.00",
        alloc_civic_y2="10.00",
        alloc_transportation_y2="10.00",
        alloc_partnerships_y2="5.00",  # total = 85, not 100
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    error_text = str(form.errors)
    assert "100%" in error_text or "100" in error_text


def test_two_year_plan_valid_with_correct_y2_allocations():
    """A two-year plan with valid Y2 allocations passes validation."""
    data = _valid_form_data(
        plan_coverage="two_year",
        fiscal_year_y2="fy_2027",
        alloc_admin_y2="10.00",
        alloc_employment_y2="10.00",
        alloc_education_y2="10.00",
        alloc_income_y2="10.00",
        alloc_housing_y2="10.00",
        alloc_health_y2="10.00",
        alloc_civic_y2="10.00",
        alloc_transportation_y2="10.00",
        alloc_partnerships_y2="20.00",  # total = 100%
    )
    form = TribalPlanFormFields(data=data)
    assert form.is_valid(), form.errors
