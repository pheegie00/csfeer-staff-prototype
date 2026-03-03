from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

from form_manager.models import FormDefinition, FormEntry, OrganizationProfile

if TYPE_CHECKING:
    from django.test.client import Client


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


@pytest.mark.django_db
def test_back_button_not_shown_on_first_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the back button is not displayed on the first page (step=0, page=0).
    This regression test ensures that current_step_number and current_page_number
    are correctly passed to the page template context.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the first page explicitly
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the back button link is not in the response
    assert "← Back" not in content

    # Verify that current_step_number and current_page_number are in the context
    assert response.context["current_step_number"] == 0
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_back_button_shown_on_second_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the back button is displayed when not on the first page.
    This verifies the back button appears for step > 0 or page > 0.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the second page
    response = authenticated_client.get(url, {"step": 1, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the back button link IS in the response
    assert "← Back" in content

    # Verify that current_step_number and current_page_number are in the context
    assert response.context["current_step_number"] == 1
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_review_back_button_accounts_for_excluded_fields(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    When fields are excluded and entire pages are removed from the UI,
    the review page back button should point to the last *visible* page,
    not the last page in the unfiltered UI definition.
    """
    edit_url = reverse("form_edit", args=[form_entry.pk])

    # Post data with NO topics selected — this excludes all cost fields
    # (item1_cost, item2_cost, item3_cost), causing the "Specific costs"
    # PageBlock to be removed entirely from the UI.
    authenticated_client.post(
        edit_url,
        data={"applicable_topics": []},
        query_params={"step": 1, "page": 0},
    )

    # Navigate to the review page
    review_url = reverse("form_review", args=[form_entry.pk])
    response = authenticated_client.get(review_url)

    assert response.status_code == 200

    prev_url = response.context["prev_url"]

    # With the "Specific costs" page removed, step 1 has only 1 page (the
    # PermanentPageBlock at index 0). So the back button should point to
    # step=1, page=0 — NOT step=1, page=1 which would cause a 500.
    expected_url = reverse(
        "form_edit",
        kwargs={"pk": form_entry.pk},
        query={"step": 1, "page": 0},
    )
    assert prev_url == expected_url


@pytest.mark.django_db
def test_save_and_exit_redirects_to_form_list(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that clicking 'Save & Exit' saves the form data and redirects to the form list.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Post data with page-action=save-exit
    response = authenticated_client.post(
        url,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "page-action": "save-exit",
        },
        query_params={
            "step": 0,
            "page": 0,
        },
    )

    # Should redirect to form_list
    assert response.status_code == 302
    assert response.headers.get("Location") == reverse("form_list")

    # Data should be saved
    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "John"
    assert form_entry.data.get("last_name") == "Doe"


@pytest.mark.django_db
def test_next_button_stays_on_form_edit(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that clicking 'Next' (without page-action=save-exit) saves the data
    but stays on the form edit page.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Post data without page-action=save-exit (simulating Next button)
    response = authenticated_client.post(
        url,
        data={
            "first_name": "Jane",
            "last_name": "Smith",
        },
        query_params={
            "step": 0,
            "page": 0,
        },
    )

    # Should return 200 (re-render the form edit page)
    assert response.status_code == 200

    # Data should be saved
    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "Jane"
    assert form_entry.data.get("last_name") == "Smith"


@pytest.mark.django_db
def test_save_and_exit_button_not_shown_on_first_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the 'Save & Exit' button is not displayed on the first page (step=0, page=0).
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the first page explicitly
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the "Save & Exit" button is not in the response
    assert "Save &amp; Exit" not in content
    assert 'value="save-exit"' not in content


@pytest.mark.django_db
def test_save_and_exit_button_shown_on_second_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the 'Save & Exit' button is displayed when not on the first page.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the second page (step 1, page 0)
    response = authenticated_client.get(url, {"step": 1, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the "Save & Exit" button IS in the response
    assert "Save &amp; Exit" in content or "Save & Exit" in content
    assert 'value="save-exit"' in content
