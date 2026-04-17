"""Integration and unit tests for TribalPlanForm."""

from typing import TYPE_CHECKING, cast

import pytest
from django import forms
from django.core.management import call_command
from django.urls import reverse

from form_manager.constants import CSBGTribalPlanApplicationForms
from form_manager.models import FormDefinition, FormEntry, OrganizationProfile
from form_manager.schema.choices import FISCAL_YEAR_CHOICES
from form_manager.schema.forms.tribal_plan import TribalPlanForm, TribalPlanFormFields
from form_manager.schema.layout import (
    AbstractPageBlock,
    AlertBoxBlock,
    ConditionalBlock,
    FieldBlock,
    FieldGroupBlock,
    SectionBlock,
    TextBlock,
)
from form_manager.schema.navigation import build_form_edit_url

if TYPE_CHECKING:
    from django.test.client import Client


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
    user, _ = create_user
    call_command("seed_demo_org", email=user.email, all=True)
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
        "authorized_official_state": "District of Columbia",
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
        "contact_state": "District of Columbia",
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
        "recognition_information_method": "manual",
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
    django_db_setup, create_user, tribal_plan_form_schema, client: "Client"
):
    """Starting a new TribalPlanForm creates a FormEntry and redirects to edit."""
    user, _ = create_user
    call_command("seed_demo_org", email=user.email, all=True)
    client.force_login(user)

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
    assert "One year plan" in content
    assert "Two year plan" in content
    assert "fiscal_year_y1" in content or "Fiscal Year" in content


def test_plan_coverage_field_uses_expected_radio_labels():
    """Plan coverage radios use the one-year/two-year plan labels shown in the UI."""
    plan_coverage_field = TribalPlanFormFields.base_fields["plan_coverage"]
    assert isinstance(plan_coverage_field, forms.ChoiceField)
    plan_coverage_choices = list(cast(list[tuple[str, str]], plan_coverage_field.choices))

    assert plan_coverage_choices == [
        ("one_year", "One year plan"),
        ("two_year", "Two year plan"),
    ]


def test_plan_coverage_uses_hidden_fiscal_year_fields_and_disabled_display_fields():
    """Plan coverage uses hidden saved values plus disabled display-only year inputs."""
    next_fiscal_year_value, next_fiscal_year_label = FISCAL_YEAR_CHOICES[1]
    following_fiscal_year_value, following_fiscal_year_label = FISCAL_YEAR_CHOICES[2]
    fiscal_year_y1 = TribalPlanFormFields.base_fields["fiscal_year_y1"]
    fiscal_year_y2 = TribalPlanFormFields.base_fields["fiscal_year_y2"]
    fiscal_year_y1_display = TribalPlanFormFields.base_fields["fiscal_year_y1_display_one_year"]
    fiscal_year_y2_display = TribalPlanFormFields.base_fields["fiscal_year_y2_display"]

    assert isinstance(fiscal_year_y1.widget, forms.HiddenInput)
    assert fiscal_year_y1.initial == next_fiscal_year_value

    assert isinstance(fiscal_year_y2.widget, forms.HiddenInput)
    assert (
        fiscal_year_y2.widget.attrs["x-bind:value"]
        == f"checked === 'two_year' ? '{following_fiscal_year_value}' : ''"
    )

    assert fiscal_year_y1_display.disabled is True
    assert fiscal_year_y1_display.initial == next_fiscal_year_label
    assert fiscal_year_y2_display.disabled is True
    assert fiscal_year_y2_display.initial == following_fiscal_year_label


def test_recognition_information_method_uses_expected_radio_labels():
    """Recognition method radios use the manual/upload labels shown in the UI."""
    recognition_method_field = TribalPlanFormFields.base_fields["recognition_information_method"]
    assert isinstance(recognition_method_field, forms.ChoiceField)
    recognition_method_choices = list(cast(list[tuple[str, str]], recognition_method_field.choices))

    assert recognition_method_choices == [
        ("manual", "Enter it manually"),
        ("upload", "Upload a file"),
    ]


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
def test_tribal_plan_form_section2_recognition_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 1, page 0 renders the recognition method options and citation prompt."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 1, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "How would you like to provide this information?" in content
    assert "Enter it manually" in content
    assert "Upload a file" in content
    assert (
        "Provide a citation to the State statute or code acknowledging State recognition" in content
    )


def test_tribal_plan_form_section3_goals_page_has_guidance_alert():
    """The goals page includes a guidance alert before the textarea field."""
    schema = TribalPlanForm.model_construct()

    goals_step = schema.ui[2]
    assert goals_step.title == "Goals and Objectives"
    assert goals_step.children is not None

    goals_page = goals_step.children[0]
    assert goals_page.children is not None
    assert len(goals_page.children) > 1

    assert isinstance(goals_page.children[0], AlertBoxBlock)
    alert = goals_page.children[0]
    assert alert.alert_type == "info"
    assert "align with the purposes of the CSBG program" in alert.message
    assert "obtaining emergency assistance" in alert.message
    assert "developing linkages to fill service gaps" in alert.message


def test_community_feedback_field_uses_section4_prompt():
    """Section 4 uses the updated community feedback question text."""
    community_feedback_field = TribalPlanFormFields.base_fields["community_feedback"]

    assert getattr(community_feedback_field, "title", None) == (
        "Did the Tribe or Tribal Organization solicit feedback from Tribal members "
        "that demonstrates evidence of public participation?"
    )


@pytest.mark.django_db
def test_tribal_plan_form_section5_y1_allocations_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 4, page 0 defaults to the single-column Year 1 allocation layout."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "Allocation requirements for CSBG funds" in content
    assert "Year one" in content
    assert "alloc_admin_y1" in content or "Administrative Funds" in content
    assert "alloc_total_y1" in content or "Year 1 Total" in content
    assert "alloc_admin_y2" not in content
    assert "Year two" not in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_two_year_plan_shows_year_two_allocations(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 4, page 0 renders both year allocation columns for a saved two-year plan."""
    tribal_plan_form_entry.data = {"plan_coverage": "two_year"}
    tribal_plan_form_entry.save(update_fields=["data"])

    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 0})

    assert response.status_code == 200
    content = response.content.decode()
    assert "Year one" in content
    assert "Year two" in content
    assert "alloc_admin_y1" in content or "Administrative Funds" in content
    assert "alloc_admin_y2" in content or "Administrative Funds" in content


@pytest.mark.django_db
def test_tribal_plan_form_section5_single_audit_review_page(
    django_db_setup, tribal_plan_form_entry: FormEntry, authenticated_client
):
    """Step 4, page 2 renders the dedicated Single Audit Review page."""
    url = reverse("form_edit", args=[tribal_plan_form_entry.pk])
    response = authenticated_client.get(url, query_params={"step": 4, "page": 2})

    assert response.status_code == 200
    content = response.content.decode()
    assert "Single Audit Review" in content
    assert "Single Audit requirements" in content
    assert "Has your Tribe or Tribal Organization completed a Single Audit?" in content
    assert "Date of audit" in content
    assert "Period start" in content
    assert "Period end" in content


def test_tribal_plan_form_section5_uses_card_field_groups():
    """The planned allocation page uses card field groups for each year."""
    schema = TribalPlanForm.model_construct()

    allocations_step = schema.ui[4]
    assert allocations_step.children is not None
    allocations_page = allocations_step.children[0]

    assert allocations_page.template_name == "form_manager/planned_allocation_page.html"
    assert allocations_page.children is not None
    page_children = allocations_page.children
    assert isinstance(page_children[0], AlertBoxBlock)
    assert isinstance(page_children[1], FieldGroupBlock)
    assert isinstance(page_children[2], FieldGroupBlock)

    year_one_group = cast(FieldGroupBlock, page_children[1])
    year_two_group = cast(FieldGroupBlock, page_children[2])

    assert year_one_group.template_name == "form_manager/planned_allocation_field_group.html"
    assert year_two_group.template_name == "form_manager/planned_allocation_field_group.html"
    assert year_one_group.title == "Year one"
    assert year_two_group.title == "Year two"


def test_tribal_plan_form_section5_single_audit_review_page_uses_alert_and_conditional_fields():
    """Section 5 includes a dedicated Single Audit Review page with an info alert."""
    schema = TribalPlanForm.model_construct()

    fiscal_controls_step = schema.ui[4]
    assert fiscal_controls_step.children is not None
    single_audit_page = fiscal_controls_step.children[2]
    assert isinstance(single_audit_page, AbstractPageBlock)

    assert single_audit_page.title == "Single Audit Review"
    assert single_audit_page.subtitle == (
        "Provide the date and time period covered by your most recent audit, if applicable."
    )
    assert single_audit_page.children is not None
    page_children = single_audit_page.children
    assert isinstance(page_children[0], AlertBoxBlock)

    alert = page_children[0]
    assert alert.heading == "Single Audit requirements"
    assert "expended less than $750,000 in total federal funds" in alert.message

    assert isinstance(page_children[1], SectionBlock)
    single_audit_section = page_children[1]
    assert single_audit_section.alpine_controller_field == "has_completed_single_audit"
    assert single_audit_section.children is not None
    section_children = single_audit_section.children
    assert isinstance(section_children[1], FieldBlock)
    assert section_children[1].field_name == "has_completed_single_audit"
    assert isinstance(section_children[2], ConditionalBlock)


def test_tribal_plan_form_section5_limitation_page_only_contains_acknowledgment():
    """The limitation page renders the notice card and acknowledgment only."""
    schema = TribalPlanForm.model_construct()

    fiscal_controls_step = schema.ui[4]
    assert fiscal_controls_step.children is not None
    limitation_page = fiscal_controls_step.children[1]
    assert isinstance(limitation_page, AbstractPageBlock)

    assert limitation_page.title == "Limitation on Use of Funds"
    assert (
        limitation_page.subtitle
        == "Review the requirement below and select the checkbox to confirm compliance."
    )
    assert limitation_page.children is not None
    page_children = limitation_page.children
    assert isinstance(page_children[0], TextBlock)
    notice_block = page_children[0]
    assert notice_block.heading == "Limitation on the Use of Funds"
    assert notice_block.template_name == "form_manager/use_of_funds_notice.html"

    assert isinstance(page_children[1], SectionBlock)
    acknowledgment_section = page_children[1]
    assert acknowledgment_section.children is not None
    section_children = acknowledgment_section.children
    assert isinstance(section_children[1], FieldBlock)
    assert (
        section_children[1].template_name
        == "form_manager/forms/use_of_funds_acknowledgment_field.html"
    )

    field_names = [
        child.field_name
        for section in page_children
        if isinstance(section, SectionBlock)
        for child in section.children or []
        if isinstance(child, FieldBlock)
    ]
    assert field_names == ["use_of_funds_acknowledgment"]
    assert (
        getattr(TribalPlanFormFields.base_fields["use_of_funds_acknowledgment"], "title", None)
        == "The Tribe or Tribal Organization acknowledges and assures compliance "
        "with Section 678F of the CSBG Act"
    )


def test_tribal_plan_form_section5_limitation_notice_renders_inert_link():
    """The limitation notice card renders the guidance link without navigation."""
    schema = TribalPlanForm.model_construct()

    fiscal_controls_step = schema.ui[4]
    assert fiscal_controls_step.children is not None
    limitation_page = fiscal_controls_step.children[1]
    assert limitation_page.children is not None
    assert isinstance(limitation_page.children[0], TextBlock)
    notice_block = limitation_page.children[0]

    content = notice_block.render()

    assert "Limitation on the Use of Funds" in content
    assert "Section 678F of the CSBG Act" in content
    assert 'href="#"' in content
    assert "x-on:click.prevent" in content


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


def test_recognition_requires_method_when_yes():
    """Recognition method is required when has_recognition = yes."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_information_method="",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_information_method" in form.errors


def test_recognition_manual_entry_requires_citation():
    """Citation is required when the manual recognition method is selected."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_information_method="manual",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_citation" in form.errors


def test_recognition_upload_method_requires_file():
    """An upload is required when the upload recognition method is selected."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_information_method="upload",
        recognition_citation="",
        recognition_upload="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "recognition_upload" in form.errors


def test_recognition_not_required_when_no():
    """No recognition fields are required when has_recognition = no."""
    data = _valid_form_data(
        has_recognition="no",
        recognition_information_method="",
        recognition_citation="",
    )
    form = TribalPlanFormFields(data=data)
    assert form.is_valid(), form.errors


def test_recognition_upload_can_use_existing_saved_file():
    """Existing saved recognition upload should satisfy the upload-path requirement."""
    data = _valid_form_data(
        has_recognition="yes",
        recognition_information_method="upload",
        recognition_citation="",
        recognition_upload="",
    )
    form = TribalPlanFormFields(
        data=data, initial={"recognition_upload": "form_uploads/entry/recognition.pdf"}
    )
    assert form.is_valid(), form.errors


def test_single_audit_details_required_when_yes():
    """Single Audit detail fields are required when the user reports completing one."""
    data = _valid_form_data(
        has_completed_single_audit="yes",
        audit_date="",
        audit_period_start="",
        audit_period_end="",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "audit_date" in form.errors
    assert "audit_period_start" in form.errors
    assert "audit_period_end" in form.errors


def test_single_audit_date_fields_use_date_picker_widget():
    """Single Audit date fields use the shared date picker component."""
    form = TribalPlanFormFields(data=_valid_form_data(has_completed_single_audit="yes"))

    audit_date_markup = form["audit_date"].as_widget()
    audit_period_start_markup = form["audit_period_start"].as_widget()
    audit_period_end_markup = form["audit_period_end"].as_widget()

    assert 'class="usa-date-picker"' in audit_date_markup
    assert 'type="date"' in audit_date_markup
    assert 'class="usa-date-picker"' in audit_period_start_markup
    assert 'type="date"' in audit_period_start_markup
    assert 'class="usa-date-picker"' in audit_period_end_markup
    assert 'type="date"' in audit_period_end_markup


def test_single_audit_date_fields_are_required():
    """Single Audit date fields are marked required by the field definitions."""
    form = TribalPlanFormFields(data=_valid_form_data(has_completed_single_audit="no"))

    assert form.fields["audit_date"].required is True
    assert form.fields["audit_period_start"].required is True
    assert form.fields["audit_period_end"].required is True


def test_two_year_plan_requires_fiscal_year_y2():
    """fiscal_year_y2 is required when plan_coverage = two_year."""
    data = _valid_form_data(
        plan_coverage="two_year",
        fiscal_year_y2="",
        # Provide Y2 allocations to isolate just the fiscal year check
        alloc_admin_y2="10.00",
        alloc_employment_y2="10.00",
        alloc_education_y2="10.00",
        alloc_income_y2="10.00",
        alloc_housing_y2="10.00",
        alloc_health_y2="10.00",
        alloc_civic_y2="10.00",
        alloc_transportation_y2="10.00",
        alloc_partnerships_y2="20.00",
    )
    form = TribalPlanFormFields(data=data)
    assert not form.is_valid()
    assert "fiscal_year_y2" in form.errors


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
