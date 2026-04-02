"""Integration tests for TribalShortForm"""

import re
from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.constants import CSBGAnnualReportForms
from form_manager.models import FormDefinition, FormEntry, OrganizationProfile
from tests.unit.form_manager.form_sidenav_test_helpers import (
    get_sidenav_href,
    get_sidenav_link_markup,
    get_sidenav_markup,
)

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
    url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(url)

    assert response.status_code == 200
    content = response.content.decode("utf-8")

    # Verify expected fields are present on the first page
    assert "org_name" in content or "Name of Tribe or Tribal Organization" in content


@pytest.mark.django_db
def test_tribal_short_form_edit_page_uses_left_rail_navigation(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    """Tribal Short Form edit pages show a left rail instead of the step indicator."""
    url = reverse("form_edit", args=[tribal_short_form_entry.pk])

    response = authenticated_client.get(url, query_params={"step": 0, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    assert 'aria-label="Form sections"' in content
    assert "usa-sidenav" in content
    assert "usa-step-indicator" not in content

    for nav_title in [
        "Section 1: Tribal Administration",
        "Section 2: Tribal Expenditures",
        "Section 3: Expenditure Narrative",
        "Review and Submit",
    ]:
        assert nav_title in content


@pytest.mark.django_db
def test_tribal_short_form_sidenav_expands_only_current_section_and_marks_current_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    tribal_short_form_entry.data = {
        "applicable_topics": [
            "employment_expenditure,employment_related_services_description",
            "housing_expenditure,housing_services_description",
        ]
    }
    tribal_short_form_entry.save(update_fields=["data"])

    url = reverse("form_edit", args=[tribal_short_form_entry.pk])

    response = authenticated_client.get(url, query_params={"step": 2, "page": 1})

    assert response.status_code == 200

    sidenav = get_sidenav_markup(response.content.decode("utf-8"))

    assert sidenav.count("usa-sidenav__sublist") == 1
    assert sidenav.count('class="usa-current"') == 2
    assert "Details on employment services" in sidenav
    assert "Details on housing services" in sidenav
    assert "Details on health services" not in sidenav


@pytest.mark.django_db
def test_tribal_short_form_top_level_sidenav_navigation_saves_draft_and_opens_first_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(edit_url, query_params={"step": 0, "page": 0})

    assert response.status_code == 200

    target_href = get_sidenav_href(
        response.content.decode("utf-8"), "Section 2: Tribal Expenditures"
    )

    response = authenticated_client.post(
        target_href,
        data={
            "org_name": "Example Tribal Nation",
            "contact_name": "Casey Example",
            "contact_title": "Program Director",
            "phone": "5551234567",
            "email": "casey@example.com",
        },
    )

    assert response.status_code == 200
    assert response.context["current_step_number"] == 1
    assert response.context["current_page_number"] == 0
    assert "applicable_topics" in response.content.decode("utf-8")

    tribal_short_form_entry.refresh_from_db()
    assert tribal_short_form_entry.data["org_name"] == "Example Tribal Nation"
    assert tribal_short_form_entry.data["contact_name"] == "Casey Example"


@pytest.mark.django_db
def test_tribal_short_form_child_sidenav_navigation_saves_draft_and_opens_selected_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    tribal_short_form_entry.data = {
        "applicable_topics": [
            "employment_expenditure,employment_related_services_description",
            "housing_expenditure,housing_services_description",
        ]
    }
    tribal_short_form_entry.save(update_fields=["data"])

    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(edit_url, query_params={"step": 2, "page": 1})

    assert response.status_code == 200

    target_href = get_sidenav_href(
        response.content.decode("utf-8"), "Details on employment services"
    )

    response = authenticated_client.post(
        target_href,
        data={
            "housing_services_description": "Housing support details saved from the current page.",
        },
    )

    assert response.status_code == 200
    assert response.context["current_step_number"] == 2
    assert response.context["current_page_number"] == 0
    assert "employment_related_services_description" in response.content.decode("utf-8")

    tribal_short_form_entry.refresh_from_db()
    assert (
        tribal_short_form_entry.data["housing_services_description"]
        == "Housing support details saved from the current page."
    )


@pytest.mark.django_db
def test_tribal_short_form_child_sidenav_navigation_falls_back_when_filter_change_hides_target_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    tribal_short_form_entry.data = {
        "applicable_topics": [
            "employment_expenditure,employment_related_services_description",
            "housing_expenditure,housing_services_description",
        ]
    }
    tribal_short_form_entry.save(update_fields=["data"])

    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(edit_url, query_params={"step": 2, "page": 1})

    assert response.status_code == 200

    target_href = get_sidenav_href(response.content.decode("utf-8"), "Details on housing services")

    response = authenticated_client.post(
        target_href,
        data={
            "applicable_topics": [
                "employment_expenditure,employment_related_services_description",
            ],
        },
    )

    assert response.status_code == 200
    assert response.context["current_step_number"] == 2
    assert response.context["current_page_number"] == 0
    content = response.content.decode("utf-8")
    assert "employment_related_services_description" in content
    assert "housing_services_description" not in content

    tribal_short_form_entry.refresh_from_db()
    assert tribal_short_form_entry.data["applicable_topics"] == [
        "employment_expenditure,employment_related_services_description",
    ]


@pytest.mark.django_db
def test_tribal_short_form_review_sidenav_navigation_saves_draft_and_opens_review(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(edit_url, query_params={"step": 0, "page": 0})

    assert response.status_code == 200

    target_href = get_sidenav_href(response.content.decode("utf-8"), "Review and Submit")

    response = authenticated_client.post(
        target_href,
        data={
            "org_name": "Draft org value",
        },
    )

    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse(
        "form_review", args=[tribal_short_form_entry.pk]
    )
    assert "Review and Submit" in response.content.decode("utf-8")

    tribal_short_form_entry.refresh_from_db()
    assert tribal_short_form_entry.data["org_name"] == "Draft org value"


@pytest.mark.django_db
def test_tribal_short_form_review_page_uses_left_rail_navigation_and_keeps_edit_links(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    review_url = reverse("form_review", args=[tribal_short_form_entry.pk])

    response = authenticated_client.get(review_url)

    assert response.status_code == 200

    content = response.content.decode("utf-8")
    sidenav = get_sidenav_markup(content)

    assert "usa-sidenav" in sidenav
    assert "usa-step-indicator" not in content
    assert sidenav.count('class="usa-current"') == 1
    review_link = get_sidenav_link_markup(content, "Review and Submit")
    assert 'class="usa-current"' in review_link
    assert 'data-save-draft-form="form-edit-form"' not in review_link
    assert "usa-sidenav__sublist" not in sidenav

    first_section_edit_url = (
        reverse("form_edit", args=[tribal_short_form_entry.pk]) + "?step=0&page=0"
    )
    assert f'href="{first_section_edit_url}"' in content

    edit_response = authenticated_client.get(first_section_edit_url)
    assert edit_response.status_code == 200
    assert edit_response.context["current_step_number"] == 0
    assert edit_response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_tribal_short_form_edit_sidenav_links_submit_the_current_form(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    edit_url = reverse("form_edit", args=[tribal_short_form_entry.pk])
    response = authenticated_client.get(edit_url, query_params={"step": 0, "page": 0})

    assert response.status_code == 200

    section_link = get_sidenav_link_markup(
        response.content.decode("utf-8"), "Section 2: Tribal Expenditures"
    )
    review_link = get_sidenav_link_markup(response.content.decode("utf-8"), "Review and Submit")

    assert 'data-save-draft-form="form-edit-form"' in section_link
    assert 'data-save-draft-form="form-edit-form"' in review_link


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
def test_tribal_short_form_section_label_renders_above_page_title_on_filter_page(
    django_db_setup, tribal_short_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_short_form_entry.pk]),
        query_params={"step": 1, "page": 0},
    )

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    assert re.search(
        (
            r"form-page-section-label[^>]*>\s*Section 2: Tribal Expenditures\s*</p>\s*"
            r"<h1[^>]*>\s*Expenditure categories\s*</h1>.*"
            r"How to select expenditure categories"
        ),
        content,
        re.DOTALL,
    )


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
