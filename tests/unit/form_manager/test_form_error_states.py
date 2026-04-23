"""
Unit tests for form error state initialization feature (bd-240).

Tests the session-based error display mechanism that shows validation errors
after users visit the review page and return to edit the form.
"""

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from form_manager.models import FormAuditTrail, FormEntry

if TYPE_CHECKING:
    from django.test.client import Client


@pytest.mark.django_db
def test_review_page_sets_show_errors_flag(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that visiting the review page sets the show_errors session flag.

    When a user visits the review page, the session should be updated with
    a flag indicating that validation errors should be displayed when they
    return to edit the form.
    """
    url = reverse("form_review", args=[form_entry.pk])

    response = authenticated_client.get(url)

    assert response.status_code == 200
    # Check that the session flag is set
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True


@pytest.mark.django_db
def test_form_edit_shows_errors_after_review_visit(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that form_edit displays validation errors after user visits review page.

    Once the show_errors flag is set in the session, the form should be bound
    with the existing data and validation should be triggered, displaying any
    errors to the user.
    """
    # Create invalid form data (empty first_name, assuming it's required)
    form_entry.data = {"first_name": "", "last_name": "Doe"}
    form_entry.save()

    # Set the session flag (simulating review page visit)
    session = authenticated_client.session
    session[f"show_errors_{form_entry.pk}"] = True
    session.save()

    # Visit the form edit page
    url = reverse("form_edit", args=[form_entry.pk])
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200

    # Check that the form in context is bound
    form = response.context["form"]
    assert form.is_bound
    # The form should have been validated
    assert hasattr(form, "errors")


@pytest.mark.django_db
def test_form_edit_no_errors_before_review_visit(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that form_edit does NOT display validation errors before review page visit.

    Without the show_errors flag, the form should be unbound (using initial data)
    and no validation should occur, even if the data would fail validation.
    """
    # Create invalid form data (empty first_name, assuming it's required)
    form_entry.data = {"first_name": "", "last_name": "Doe"}
    form_entry.save()

    # Visit the form edit page WITHOUT visiting review first
    # (no session flag set)
    url = reverse("form_edit", args=[form_entry.pk])
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200

    # Check that the form in context is unbound (initial data only)
    form = response.context["form"]
    assert not form.is_bound
    # Unbound forms don't have errors
    assert not form.errors


@pytest.mark.django_db
def test_form_finalize_clears_show_errors_flag(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that finalizing/submitting the form clears the show_errors session flag.

    After successful form submission, the session flag should be cleared so that
    errors don't automatically appear if the user views the form again later.
    """
    # Set valid form data
    form_entry.data = {"first_name": "John", "last_name": "Doe"}
    form_entry.save()

    # Set the session flag
    session = authenticated_client.session
    session[f"show_errors_{form_entry.pk}"] = True
    session.save()

    # Verify the flag is set before submission
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True

    # Submit the form
    url = reverse("form_finalize", args=[form_entry.pk])
    response = authenticated_client.post(url)

    # Check that the flag is cleared from session
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is None

    # Check redirect to preview page
    assert response.status_code == 302
    form_entry.refresh_from_db()
    assert form_entry.status == "submitted"
    audit = FormAuditTrail.objects.get(form_entry=form_entry)
    assert audit.action == "submit"


@pytest.mark.django_db
def test_show_errors_persists_across_pages(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that the show_errors flag persists when navigating between form pages.

    The session flag should remain set as users navigate through different
    steps and pages of the form, ensuring errors are consistently displayed.
    """
    # Set the session flag
    session = authenticated_client.session
    session[f"show_errors_{form_entry.pk}"] = True
    session.save()

    url = reverse("form_edit", args=[form_entry.pk])

    # Visit first page
    response1 = authenticated_client.get(url, {"step": 0, "page": 0})
    assert response1.status_code == 200
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True

    # Visit second page
    response2 = authenticated_client.get(url, {"step": 1, "page": 0})
    assert response2.status_code == 200
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True

    # Visit different step
    response3 = authenticated_client.get(url, {"step": 0, "page": 0})
    assert response3.status_code == 200
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True


@pytest.mark.django_db
def test_show_errors_with_empty_data(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client"
):
    """
    Test that error display handles entries with no data gracefully.

    When entry.data is None or empty, the form should still render without
    crashing, even when show_errors flag is set.
    """
    # Ensure entry has no data
    form_entry.data = {}
    form_entry.save()

    # Set the session flag
    session = authenticated_client.session
    session[f"show_errors_{form_entry.pk}"] = True
    session.save()

    # Visit the form edit page
    url = reverse("form_edit", args=[form_entry.pk])
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    # Should still render successfully
    assert response.status_code == 200

    # Form should be unbound since entry.data is falsy
    form = response.context["form"]
    assert not form.is_bound


@pytest.mark.django_db
def test_session_flag_isolated_per_entry(
    django_db_setup, form_entry: FormEntry, authenticated_client: "Client", seed_data
):
    """
    Test that the show_errors flag is isolated per form entry.

    Each form entry should have its own session flag, ensuring that visiting
    the review page for one form doesn't affect error display for other forms.
    """
    from organizations.models import OrganizationProfile
    from form_manager.models import FormDefinition

    user, _ = seed_data

    # Create a second form entry
    org = OrganizationProfile.objects.create(
        name="test org 2",
        address="123 Main Street, Washington, DC",
        contact_email="info@myorg.org",
        contact_phone="123=456-7890",
    )

    form_def = FormDefinition.objects.first()

    second_entry = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=user,
        version_number="1",
        data={"first_name": "Jane", "last_name": "Smith"},
    )

    # Set the session flag for first entry only
    session = authenticated_client.session
    session[f"show_errors_{form_entry.pk}"] = True
    session.save()

    # Check that first entry has flag set
    assert authenticated_client.session.get(f"show_errors_{form_entry.pk}") is True

    # Check that second entry does NOT have flag set
    assert authenticated_client.session.get(f"show_errors_{second_entry.pk}") is None

    # Visit first entry - should show errors (if form is bound)
    url1 = reverse("form_edit", args=[form_entry.pk])
    response1 = authenticated_client.get(url1, {"step": 0, "page": 0})
    assert response1.status_code == 200

    # Visit second entry - should NOT show errors
    url2 = reverse("form_edit", args=[second_entry.pk])
    response2 = authenticated_client.get(url2, {"step": 0, "page": 0})
    assert response2.status_code == 200

    form2 = response2.context["form"]
    # Second form should be unbound since its flag is not set
    assert not form2.is_bound
