"""
End-to-end tests for calculated field functionality.

Tests that calculated fields (CalculatedField and CalculatedCurrencyField)
automatically update when source field values change.
"""

import pytest
from playwright.sync_api import Page


def fill_and_verify_total(page: Page, field_label: str, amount: str, expected_total: str):
    """
    Fill an expenditure field and verify the total updates correctly.

    Args:
        page: Playwright Page object
        field_label: Label text of the field to fill
        amount: Value to enter in the field
        expected_total: Expected value in the total_expenditures field after calculation
    """
    field = page.get_by_label(field_label)
    field.fill(amount)
    field.blur()
    page.wait_for_timeout(500)  # Allow JavaScript to process change event

    total_field = page.locator('input[name="total_expenditures"]')
    actual_total = total_field.input_value()

    assert actual_total == expected_total, (
        f"After setting {field_label} to {amount}, "
        f"expected total {expected_total}, but got {actual_total}"
    )


@pytest.mark.e2e
@pytest.mark.auth
def test_calculated_currency_field_auto_updates(authenticated_page: Page, base_url: str) -> None:
    """
    Test that calculated currency fields automatically update when source fields change.

    This test verifies the JavaScript functionality in updateCalculatedFields():
    1. Initial calculated field starts at 0.00
    2. Calculated field updates after entering first value
    3. Calculated field recalculates when additional values are added
    4. Calculated field recalculates when existing values are changed
    5. Format is correct (comma separators, 2 decimal places)
    6. Handles edge cases (empty fields, zero values)
    """
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start new TribalShortForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_text("Start New Form").click()
            break

    # Wait for form to load - Step 1 of 4: Basic Information
    page.wait_for_selector('h4:has-text("Step 1 of 4 Basic Information")')

    # Fill minimal required data for Step 1
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Calculated Field Test")
    page.get_by_label("Full name *").fill("Test User")
    page.get_by_label("Role *").fill("Tester")
    page.get_by_label("Primary phone number *").fill("555-0000")
    page.get_by_label("Email address *").fill("test@example.org")

    # Continue to Step 2: Expenditure categories
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Save & Continue →").click()

    # Wait for Step 2 to load
    page.wait_for_selector('h4:has-text("Step 2 of 4 Expenditure categories")')

    # Select expenditure categories to reveal amount fields
    # Use JavaScript to click checkboxes (works with Alpine.js)
    page.evaluate(
        """
        () => {
            const checkboxSelectors = [
                'input[type="checkbox"][value*="employment"]',
                'input[type="checkbox"][value*="housing"]',
                'input[type="checkbox"][value*="childcare"]'
            ];

            checkboxSelectors.forEach(selector => {
                const checkbox = document.querySelector(selector);
                if (checkbox) {
                    const label = document.querySelector(`label[for="${checkbox.id}"]`);
                    if (label) label.click();
                }
            });
        }
    """
    )

    # Wait for Alpine.js to process the changes
    page.wait_for_timeout(1000)

    # Continue to expenditure amounts page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Save & Continue →").click()
    page.wait_for_timeout(1000)

    # Verify we're on the expenditure amounts page
    body_text = page.evaluate("() => document.body.innerText")
    assert "Provide the amounts" in body_text

    # Locate the total expenditures field
    total_field = page.locator('input[name="total_expenditures"]')

    # Test 1: Verify initial state (should be 0.00 or empty)
    initial_value = total_field.input_value()
    assert initial_value in [
        "",
        "0.00",
    ], f"Expected initial value to be empty or 0.00, got {initial_value}"

    # Test 2: Auto-calculation on first entry
    fill_and_verify_total(page, "Employment *", "50000", "50,000.00")

    # Test 3: Auto-calculation on second entry (accumulation)
    fill_and_verify_total(page, "Housing *", "25000", "75,000.00")

    # Test 4: Auto-calculation on third entry
    fill_and_verify_total(
        page,
        "Childcare",
        "15000",
        "90,000.00",
    )

    # Test 5: Recalculation when existing value changes
    employment_field = page.get_by_label("Employment *")
    employment_field.clear()
    employment_field.fill("60000")
    employment_field.blur()
    page.wait_for_timeout(500)
    assert (
        total_field.input_value() == "100,000.00"
    ), "Total should update to 100,000.00 after changing Employment"

    # Test 6: Edge case - clearing a field
    housing_field = page.get_by_label("Housing *")
    housing_field.clear()
    housing_field.blur()
    page.wait_for_timeout(500)
    assert (
        total_field.input_value() == "75,000.00"
    ), "Total should be 75,000.00 after clearing Housing field"

    # Test 7: Edge case - entering zero
    housing_field.fill("0")
    housing_field.blur()
    page.wait_for_timeout(500)
    assert (
        total_field.input_value() == "75,000.00"
    ), "Total should remain 75,000.00 when Housing is 0"

    # Test 8: Edge case - large numbers with proper formatting
    housing_field.clear()
    housing_field.fill("999999.99")
    housing_field.blur()
    page.wait_for_timeout(500)
    # 60000 + 999999.99 + 15000 = 1074999.99
    assert (
        total_field.input_value() == "1,074,999.99"
    ), "Total should handle large numbers with comma separators"

    # Test 9: Verify field is disabled (read-only)
    is_disabled = total_field.is_disabled()
    assert is_disabled, "Calculated field should be disabled (read-only)"

    # Success - calculated field updates correctly!
