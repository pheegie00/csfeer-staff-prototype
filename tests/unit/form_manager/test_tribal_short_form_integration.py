"""Integration tests for TribalShortForm"""

from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.constants import CSBGAnnualReportForms
from organizations.models import OrganizationProfile
from form_manager.models import FormDefinition, FormEntry
from form_manager.schema.navigation import build_form_edit_url

if TYPE_CHECKING:
    from django.test.client import Client


@pytest.fixture
def tribal_short_form_schema(django_db_setup):
    """Fixture that ensures TribalShortForm schema is loaded"""
    call_command("load_initial_forms")

    form_def = FormDefinition.objects.get(name=CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT)
    return form_def


@pytest.fixture
def tribal_short_form_entry(create_user, tribal_short_form_schema) -> FormEntry:
    """Create a TribalShortForm entry for testing"""
    user, user_details = create_user

    # Seed organization
    call_command("seed_demo_org", email=user.email, all=True)

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    entry = FormEntry.objects.create(
        form_definition=tribal_short_form_schema,
        organization=org,
        created_by=user,
        version_number="1",
        # Must be non-empty; an empty selection excludes all Section 3
        # fields, leaving it with no pages.
        data={
            "applicable_topics": ["employment_expenditure,employment_related_services_description"]
        },
    )

    return entry


@pytest.mark.django_db
def test_can_start_tribal_short_form(
    django_db_setup, create_user, tribal_short_form_schema, client: "Client"
):
    """Test starting a new TribalShortForm entry"""
    user, details = create_user

    # Seed org
    call_command("seed_demo_org", email=user.email, all=True)

    client.force_login(user)

    url = reverse("form_start", args=[tribal_short_form_schema.pk])
    response = client.get(url)

    assert response.status_code == 302
    assert FormEntry.objects.count() == 1

    entry = FormEntry.objects.first()
    assert entry
    assert entry.form_definition == tribal_short_form_schema
    assert response.headers.get("Location", "") == reverse("form_edit", args=[entry.pk])


@pytest.mark.django_db
def test_tribal_short_form_renders(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Test that TribalShortForm renders correctly"""
    url = build_form_edit_url(tribal_short_form_entry.pk, step_number=0, page_number=0)
    response = authenticated_client.get(url)

    assert response.status_code == 200
    content = response.content.decode("utf-8")

    # Verify expected fields are present on the first page
    assert "org_name" in content or "Name of Tribe or Tribal Organization" in content


@pytest.mark.django_db
def test_tribal_short_form_basic_info_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Test that TribalShortForm basic information page renders correctly"""
    url = reverse("form_edit", args=[tribal_short_form_entry.pk])

    # GET the first page (Basic Information)
    response = authenticated_client.get(
        url,
        query_params={
            "step": 0,
            "page": 0,
        },
    )

    assert response.status_code == 200
    content = response.content.decode("utf-8")

    # Verify basic information fields are present
    assert "org_name" in content or "Name of Tribe" in content
    assert "contact_name" in content or "Full name" in content
    assert "email" in content or "Email address" in content


@pytest.mark.django_db
def test_tribal_short_form_filter_page_renders(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Test that field filter page renders correctly in TribalShortForm"""
    url = reverse("form_edit", args=[tribal_short_form_entry.pk])

    # Navigate to the filter page (step 1, page 0)
    response = authenticated_client.get(
        url,
        query_params={
            "step": 1,
            "page": 0,
        },
    )

    assert response.status_code == 200
    content = response.content.decode("utf-8")

    # Verify applicable_topics filter field is present
    assert "applicable_topics" in content or "Expenditure categories" in content


@pytest.mark.django_db
def test_tribal_short_form_expenditure_page_renders(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Test that expenditure amounts page renders correctly"""

    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])

    # Get the expenditure amounts page (step 1, page 1)
    response = authenticated_client.get(
        edit_url,
        query_params={"step": 1, "page": 1},
    )

    assert response.status_code == 200
    content = response.content.decode("utf-8")

    # Verify expenditure fields are present
    assert (
        "employment_expenditure" in content
        or "childcare_expenditure" in content
        or "Expenditure" in content
    )


@pytest.mark.django_db
def test_tribal_short_form_no_demographic_fields(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Verify that demographic fields are not present in any step"""
    # Check that demographic fields are not in the form fields
    from form_manager.schema.forms.tribal_short_form import TribalShortFormFields

    form = TribalShortFormFields()
    field_names = list(form.fields.keys())

    demographic_field_names = [
        "total_individuals_served",
        "total_individuals_served_over_18",
        "male_individuals_served",
        "female_individuals_served",
        "total_individuals_served_by_sex",
        "employment__full_time",
        "employment__part_time",
        "employment__migrant_seasonal",
        "employment__unemployed_short_term",
        "employment__unemployed_long_term",
        "employment__permanently_unemployed",
        "employment__retired",
        "employment__unknown",
        "employment__total",
    ]

    # Ensure none of the demographic fields are in the form
    for field_name in demographic_field_names:
        assert (
            field_name not in field_names
        ), f"Demographic field {field_name} should not be in short form"
