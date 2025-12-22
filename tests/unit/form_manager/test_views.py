from typing import TYPE_CHECKING

import pytest
from django.core.management import call_command
from django.urls import reverse

from form_manager.models import FormDefinition, FormEntry, OrganizationProfile

if TYPE_CHECKING:
    from django.test.client import Client


MODULE_PATH = "form_manager.management.commands.load_initial_forms"


@pytest.fixture
def seed_data(create_user):
    user, details = create_user

    call_command("load_initial_forms")
    call_command("seed_demo_org", email=user.email, all=True)

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

    assert response.headers.get("Location", "") == reverse("form_edit_legacy", args=[obj.pk])


@pytest.mark.django_db
def test_can_render_and_edit_form(django_db_setup, form_entry: "FormEntry", authenticated_client):
    """Ensure the load_initial_forms command loads successfully."""

    url = reverse("form_edit_legacy", args=[form_entry.pk])

    response = authenticated_client.get(url)

    assert response.status_code == 200
