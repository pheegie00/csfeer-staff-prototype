from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.models import FormDefinition, FormEntry, OrganizationProfile

if TYPE_CHECKING:
    from django.test.client import Client


@pytest.fixture
def seed_data(create_user, use_test_schema):
    user, details = create_user

    call_command("seed_demo_org", email=user.email, all=True)
    call_command("load_initial_forms")

    return user, details


@pytest.fixture
def form_entry(seed_data, create_user) -> FormEntry:

    user, user_details = create_user

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    form_def = FormDefinition.objects.first()

    entry = FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=user, version_number="1"
    )

    return entry


@pytest.mark.django_db
def test_can_start_new_form(django_db_setup, seed_data, client: "Client"):
    """Ensure the load_initial_forms command loads successfully."""

    user, details = seed_data

    client.force_login(user)

    form = FormDefinition.objects.all().first()

    assert form

    url = reverse("form_start", args=[form.pk])

    response = client.get(url)

    assert response.status_code == 302
    assert FormEntry.objects.count() == 1

    obj = FormEntry.objects.first()

    assert obj

    assert response.headers.get("Location", "") == reverse("form_edit", args=[obj.pk])


@pytest.mark.django_db
def test_can_render_and_edit_form(django_db_setup, form_entry: "FormEntry", authenticated_client):
    """Ensure the load_initial_forms command loads successfully."""

    url = reverse("form_edit", args=[form_entry.pk])

    response = authenticated_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_can_correctly_filter_fields(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """Ensure the load_initial_forms command loads successfully."""

    url = reverse("form_edit", args=[form_entry.pk])

    # Make a GET request to the form's first page
    response = authenticated_client.get(url)

    # It should be a 200 response
    assert response.status_code == 200

    # Now post some data for the first page
    response = authenticated_client.post(
        url,
        data={
            "first_name": "Steven",
            "last_name": "Jones",
        },
        query_params={
            "step": 1,
            "page": 0,
        },
    )

    # It should be a 200 response
    assert response.status_code == 200

    # The data should have been saved
    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "Steven"
    assert form_entry.data.get("last_name") == "Jones"

    # Make a post request to choose the applicable fields
    response = authenticated_client.post(
        url,
        data={
            "applicable_topics": ["item1_cost", "item2_cost"],
        },
        query_params={
            "step": 1,
            "page": 1,
        },
    )

    # It should be a 200 response
    assert response.status_code == 200

    # there should be a field for item 1 and item 2 in the response
    assert "item1_cost" in response.content.decode("utf-8")
    assert "item2_cost" in response.content.decode("utf-8")

    # but the item 3 field should not be in the response
    assert "item3_cost" not in response.content.decode("utf-8")
