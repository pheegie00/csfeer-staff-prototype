from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.constants import CSBGAnnualReportForms
from form_manager.models import FormDefinition, FormEntry, OrganizationProfile

if TYPE_CHECKING:
    from django.test.client import Client


@pytest.fixture
def tribal_form_entry_factory(create_user):
    user, _ = create_user

    call_command("load_initial_forms")
    call_command("seed_demo_org", email=user.email, all=True)

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()
    assert org is not None

    def create_entry(form_name: CSBGAnnualReportForms) -> FormEntry:
        form_definition = FormDefinition.objects.get(name=form_name)
        return FormEntry.objects.create(
            form_definition=form_definition,
            organization=org,
            created_by=user,
            version_number="1",
        )

    return create_entry


@pytest.fixture
def tribal_short_form_entry(tribal_form_entry_factory) -> FormEntry:
    return tribal_form_entry_factory(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT)


@pytest.fixture
def tribal_long_form_entry(tribal_form_entry_factory) -> FormEntry:
    return tribal_form_entry_factory(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0)


@pytest.mark.django_db
def test_short_form_edit_page_renders_default_sidenav(
    tribal_short_form_entry: FormEntry, authenticated_client: "Client"
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_short_form_entry.pk]),
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200

    content = response.content.decode("utf-8")
    side_nav_items = response.context["side_nav_items"]

    assert 'nav aria-label="Form sections"' in content
    assert "usa-step-indicator" not in content
    assert "Section 1: Basic Information" in content
    assert "Your basic information" in content
    assert "Review &amp; Submit" in content
    assert len(side_nav_items) == 4
    assert side_nav_items[0]["label"] == "Section 1: Basic Information"
    assert side_nav_items[0]["is_current"] is True
    assert side_nav_items[0]["is_expanded"] is True
    assert side_nav_items[0]["children"][0]["label"] == "Your basic information"
    assert side_nav_items[0]["children"][0]["is_current"] is True
    assert side_nav_items[-1]["label"] == "Review & Submit"
    assert side_nav_items[-1]["is_current"] is False


@pytest.mark.django_db
def test_long_form_edit_page_expands_only_current_section(
    tribal_long_form_entry: FormEntry, authenticated_client: "Client"
):
    response = authenticated_client.get(
        reverse("form_edit", args=[tribal_long_form_entry.pk]),
        query_params={"step": 2, "page": 0},
    )

    assert response.status_code == 200

    content = response.content.decode("utf-8")
    side_nav_items = response.context["side_nav_items"]

    assert "Section 3: Expenditure details" in content
    assert "Details on employment services" in content
    assert "Details on education services" in content
    assert "Let&#x27;s collect demographic details" not in content
    assert side_nav_items[2]["is_current"] is True
    assert side_nav_items[2]["is_expanded"] is True
    assert side_nav_items[2]["children"][0]["is_current"] is True
    assert side_nav_items[3]["is_current"] is False
    assert side_nav_items[3]["is_expanded"] is False


@pytest.mark.django_db
def test_review_page_marks_review_as_current_in_sidenav(
    tribal_short_form_entry: FormEntry, authenticated_client: "Client"
):
    response = authenticated_client.get(reverse("form_review", args=[tribal_short_form_entry.pk]))

    assert response.status_code == 200

    content = response.content.decode("utf-8")
    side_nav_items = response.context["side_nav_items"]

    assert 'nav aria-label="Form sections"' in content
    assert "usa-step-indicator" not in content
    assert "Review &amp; Submit" in content
    assert side_nav_items[-1]["is_current"] is True
    assert all(item["is_current"] is False for item in side_nav_items[:-1])
    assert all(item["is_expanded"] is False for item in side_nav_items[:-1])
