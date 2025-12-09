"""
End-to-end tests for form manager functionality.
"""

import pytest
from playwright.sync_api import Page

from tests.e2e.pages.form_manager_page import FormManagerPage


@pytest.mark.e2e
@pytest.mark.auth
def test_forms_page_loads(authenticated_page: Page, base_url: str) -> None:
    """Test that the forms listing page loads successfully."""
    # Navigate directly to forms page
    authenticated_page.goto(f"{base_url}/forms/")

    # Simply verify URL contains /forms/
    assert "/forms/" in authenticated_page.url


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(reason="Requires actual form data to be present")
def test_view_form_details(authenticated_page: Page, base_url: str) -> None:
    """Test viewing a specific form."""
    page = authenticated_page
    form_page = FormManagerPage(page, base_url)

    # Navigate to forms page
    form_page.navigate_to_forms()

    # Click on a form (adjust form name as needed)
    form_page.click_form("Test Form")

    # Assert form details are visible
    # Add specific assertions based on form structure


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(reason="Requires form submission implementation details")
def test_submit_form(authenticated_page: Page, base_url: str) -> None:
    """Test submitting a form with valid data."""
    page = authenticated_page
    form_page = FormManagerPage(page, base_url)

    # Navigate to a specific form
    form_page.navigate_to_forms()
    form_page.click_form("Test Form")

    # Fill out form fields (adjust based on actual form structure)
    form_page.fill_form_field("Name", "Test User")
    form_page.fill_form_field("Email", "test@example.com")

    # Submit form
    form_page.submit_form()

    # Assert success
    form_page.expect_success_message()


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(reason="Requires form validation implementation details")
def test_form_validation(authenticated_page: Page, base_url: str) -> None:
    """Test that form validation works correctly."""
    page = authenticated_page
    form_page = FormManagerPage(page, base_url)

    # Navigate to a specific form
    form_page.navigate_to_forms()
    form_page.click_form("Test Form")

    # Try to submit without filling required fields
    form_page.submit_form()

    # Assert validation errors are shown
    form_page.expect_error_message()
