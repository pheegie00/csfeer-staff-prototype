"""Integration tests for TribalLongForm"""

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


@pytest.fixture
def tribal_long_form_schema(django_db_setup):
    call_command("load_initial_forms")

    return FormDefinition.objects.get(name=CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0)


@pytest.fixture
def tribal_long_form_entry(create_user, tribal_long_form_schema) -> FormEntry:
    user, user_details = create_user

    call_command("seed_demo_org", email=user.email, all=True)

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    return FormEntry.objects.create(
        form_definition=tribal_long_form_schema,
        organization=org,
        created_by=user,
        version_number="1",
    )


@pytest.mark.django_db
def test_tribal_long_form_edit_page_uses_left_rail_navigation(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    assert 'aria-label="Form sections"' in content
    assert "usa-sidenav" in content
    assert "usa-step-indicator" not in content

    for nav_title in [
        "Basic Information",
        "Expenditure categories",
        "Expenditure details",
        "Demographic information",
        "Review and Submit",
    ]:
        assert nav_title in content


@pytest.mark.django_db
def test_tribal_long_form_sidenav_expands_only_current_section_and_marks_current_page(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    tribal_long_form_entry.data = {
        "applicable_topics": [
            "employment_expenditure,employment_related_services_description",
            "housing_expenditure,housing_services_description",
        ]
    }
    tribal_long_form_entry.save(update_fields=["data"])

    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 2, "page": 1},
    )

    assert response.status_code == 200

    sidenav = get_sidenav_markup(response.content.decode("utf-8"))

    assert sidenav.count("usa-sidenav__sublist") == 1
    assert sidenav.count('class="usa-current"') == 2
    assert "Details on employment services" in sidenav
    assert "Details on housing services" in sidenav
    assert "Details on health services" not in sidenav


@pytest.mark.django_db
def test_tribal_long_form_top_level_sidenav_navigation_saves_draft_and_opens_first_page(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200

    target_href = get_sidenav_href(response.content.decode("utf-8"), "Demographic information")

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
    assert response.context["current_step_number"] == 3
    assert response.context["current_page_number"] == 0
    assert "total_individuals_served" in response.content.decode("utf-8")

    tribal_long_form_entry.refresh_from_db()
    assert tribal_long_form_entry.data["org_name"] == "Example Tribal Nation"
    assert tribal_long_form_entry.data["contact_name"] == "Casey Example"


@pytest.mark.django_db
def test_tribal_long_form_child_sidenav_navigation_saves_draft_and_opens_selected_page(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    tribal_long_form_entry.data = {
        "applicable_topics": [
            "employment_expenditure,employment_related_services_description",
            "housing_expenditure,housing_services_description",
        ]
    }
    tribal_long_form_entry.save(update_fields=["data"])

    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 2, "page": 1},
    )

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

    tribal_long_form_entry.refresh_from_db()
    assert (
        tribal_long_form_entry.data["housing_services_description"]
        == "Housing support details saved from the current page."
    )


@pytest.mark.django_db
def test_tribal_long_form_review_sidenav_navigation_saves_draft_and_opens_review(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200

    target_href = get_sidenav_href(response.content.decode("utf-8"), "Review and Submit")

    response = authenticated_client.post(
        target_href,
        data={
            "org_name": "Draft org value",
        },
    )

    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse("form_review", args=[tribal_long_form_entry.pk])
    assert "Review and Submit" in response.content.decode("utf-8")

    tribal_long_form_entry.refresh_from_db()
    assert tribal_long_form_entry.data["org_name"] == "Draft org value"


@pytest.mark.django_db
def test_tribal_long_form_review_page_uses_left_rail_navigation_and_keeps_edit_links(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(reverse("form_review", args=[tribal_long_form_entry.pk]))

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
        reverse("form_edit", args=[tribal_long_form_entry.pk]) + "?step=0&page=0"
    )
    assert f'href="{first_section_edit_url}"' in content

    edit_response = authenticated_client.get(first_section_edit_url)
    assert edit_response.status_code == 200
    assert edit_response.context["current_step_number"] == 0
    assert edit_response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_tribal_long_form_edit_sidenav_links_submit_the_current_form(
    django_db_setup, tribal_long_form_entry: "FormEntry", authenticated_client
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200

    section_link = get_sidenav_link_markup(
        response.content.decode("utf-8"), "Demographic information"
    )
    review_link = get_sidenav_link_markup(response.content.decode("utf-8"), "Review and Submit")

    assert 'data-save-draft-form="form-edit-form"' in section_link
    assert 'data-save-draft-form="form-edit-form"' in review_link
