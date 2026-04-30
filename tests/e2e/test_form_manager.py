"""
End-to-end tests for form manager functionality.
"""

import pytest
from playwright.sync_api import Page


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
def test_clearing_field_value_persists(authenticated_page: Page, base_url: str) -> None:
    """Test clearing a field value persists and Save & Exit returns to the forms list."""
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start new TribalShortForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    page.get_by_role("heading", name="Your basic information").wait_for()

    # Fill the "Name of Tribe" field
    tribe_name_field = page.get_by_label("Name of Tribe or Tribal Organization *")
    tribe_name_field.fill("Test Organization For Clearing")

    # Fill other required fields
    page.get_by_label("Full name *").fill("Test User")
    page.get_by_label("Title *").fill("Tester")
    page.get_by_label("Primary phone number *").fill("555-0000")
    page.get_by_label("Email address *").fill("test@example.org")

    # Next
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()

    page.get_by_text("Select all that apply:").wait_for()

    # Go back to Step 1
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_text("← Back").click()

    page.get_by_role("heading", name="Your basic information").wait_for()

    # Verify the field still has the value
    tribe_name_value = tribe_name_field.input_value()
    assert tribe_name_value == "Test Organization For Clearing"

    # Clear the field
    tribe_name_field.clear()
    tribe_name_field.blur()
    page.wait_for_timeout(300)

    # Verify field is empty
    assert tribe_name_field.input_value() == ""

    # Next
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Next →").click()

    page.get_by_text("Select all that apply:").wait_for()

    # Go back to Step 1 again to verify the cleared value persisted
    page.get_by_text("← Back").click()
    page.get_by_role("heading", name="Your basic information").wait_for()

    # Verify the field is still empty (the bug would cause it to show the old value)
    final_value = tribe_name_field.input_value()
    assert final_value == "", f"Expected empty field, but got: {final_value}"

    # Now go forward to Step 2 and test Save & Exit button
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Next →").click()

    page.get_by_text("Select all that apply:").wait_for()

    # Scroll to bottom and click "Save & Exit" button
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Save & Exit").click()

    # Should return to the form list page
    page.wait_for_load_state("networkidle")
    assert "/forms/" in page.url
    assert "/edit" not in page.url
