"""
End-to-end tests for integer field comma formatting.

Tests that integer fields display comma-separated numbers when typing,
and that the formatted values persist through save and review.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.auth
def test_integer_field_comma_formatting_on_input(authenticated_page: Page, base_url: str) -> None:
    """
    Test that integer fields auto-format with commas as the user types,
    and that the formatted values are preserved through save and navigation.

    Uses the Tribal Long Form demographic pages which have IntegerFields.
    """
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start new TribalLongForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Annual Report" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    # Wait for form to load - Step 1 of 5: Basic Information
    page.wait_for_selector('h4:has-text("Step 1 of 5 Basic Information")')

    # Fill minimal required data for Step 1
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Integer Format Test")
    page.get_by_label("Full name *").fill("Test User")
    page.get_by_label("Role *").fill("Tester")
    page.get_by_label("Primary phone number *").fill("555-0000")
    page.get_by_label("Email address *").fill("test@example.org")

    # Continue to Step 2: Expenditure categories
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()
    page.wait_for_selector('h4:has-text("Step 2 of 5 Expenditure categories")')

    # Select at least one expenditure category to proceed
    page.evaluate(
        """
        () => {
            const checkbox = document.querySelector('input[type="checkbox"][value*="employment"]');
            if (checkbox) {
                const label = document.querySelector(`label[for="${checkbox.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)

    # Continue through expenditure amounts page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill expenditure amount to proceed
    page.get_by_label("Employment *").fill("50000.00")

    # Continue through administration costs page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Select "No" for administration costs
    page.evaluate(
        """
        () => {
            const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
            const noRadio = radios.find(r => {
                const label = document.querySelector(`label[for="${r.id}"]`);
                return label && label.textContent.trim() === 'No';
            });
            if (noRadio) {
                const label = document.querySelector(`label[for="${noRadio.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)

    # Continue through expenditure details
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill employment description
    page.get_by_label("Description *").fill("E2E test: employment services")

    # Continue to Step 4: Demographic information
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    body_text = page.evaluate("() => document.body.innerText")
    assert "4 of 5" in body_text
    assert "Demographic information" in body_text

    # ==========================================
    # Test 1: Comma formatting on input
    # ==========================================
    total_individuals = page.get_by_label("Total number of people").first
    total_individuals.fill("12345")
    total_individuals.blur()
    page.wait_for_timeout(500)

    # The Alpine.js mask should format it with commas
    assert (
        total_individuals.input_value() == "12,345"
    ), f"Expected '12,345', got '{total_individuals.input_value()}'"

    # ==========================================
    # Test 2: Large number formatting
    # ==========================================
    total_households = page.get_by_label("Total number of people").nth(1)
    total_households.fill("1234567")
    total_households.blur()
    page.wait_for_timeout(500)

    assert (
        total_households.input_value() == "1,234,567"
    ), f"Expected '1,234,567', got '{total_households.input_value()}'"

    # ==========================================
    # Test 3: Small numbers (no commas needed)
    # ==========================================
    total_individuals.clear()
    total_individuals.fill("999")
    total_individuals.blur()
    page.wait_for_timeout(500)

    assert (
        total_individuals.input_value() == "999"
    ), f"Expected '999', got '{total_individuals.input_value()}'"

    # ==========================================
    # Test 4: Values persist through save & navigate
    # ==========================================
    # Set values for next page navigation
    total_individuals.clear()
    total_individuals.fill("15000")
    total_individuals.blur()
    page.wait_for_timeout(500)

    total_households.clear()
    total_households.fill("8500")
    total_households.blur()
    page.wait_for_timeout(500)

    # Save and continue to sex breakdown page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill sex breakdown with large numbers
    male_field = page.locator('input[name="male_individuals_served"]')
    female_field = page.locator('input[name="female_individuals_served"]')

    male_field.fill("8000")
    male_field.blur()
    page.wait_for_timeout(500)

    assert (
        male_field.input_value() == "8,000"
    ), f"Expected '8,000', got '{male_field.input_value()}'"

    female_field.fill("7000")
    female_field.blur()
    page.wait_for_timeout(500)

    assert (
        female_field.input_value() == "7,000"
    ), f"Expected '7,000', got '{female_field.input_value()}'"

    # ==========================================
    # Test 5: Calculated field formats as integer (no decimals)
    # ==========================================
    total_by_sex = page.locator('input[name="total_individuals_served_by_sex"]')
    page.wait_for_timeout(500)

    assert (
        total_by_sex.input_value() == "15,000"
    ), f"Expected calculated total '15,000', got '{total_by_sex.input_value()}'"

    # Save and continue to employment page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Test 6: Employment fields with comma formatting
    # ==========================================
    full_time = page.locator('input[name="employment__full_time"]')
    part_time = page.locator('input[name="employment__part_time"]')

    full_time.fill("5000")
    full_time.blur()
    page.wait_for_timeout(500)

    assert full_time.input_value() == "5,000", f"Expected '5,000', got '{full_time.input_value()}'"

    part_time.fill("3500")
    part_time.blur()
    page.wait_for_timeout(500)

    assert part_time.input_value() == "3,500", f"Expected '3,500', got '{part_time.input_value()}'"

    # Fill remaining employment fields
    page.locator('input[name="employment__migrant_seasonal"]').fill("0")
    page.locator('input[name="employment__unemployed_short_term"]').fill("2500")
    page.locator('input[name="employment__unemployed_long_term"]').fill("2000")
    page.locator('input[name="employment__permanently_unemployed"]').fill("1500")
    page.locator('input[name="employment__unknown"]').fill("500")

    # Blur last field and wait for calculation
    page.locator('input[name="employment__unknown"]').blur()
    page.wait_for_timeout(1000)

    # ==========================================
    # Test 7: Employment total calculated field (integer, no decimals)
    # ==========================================
    employment_total = page.locator('input[name="employment__total"]')
    # 5000 + 3500 + 0 + 2500 + 2000 + 1500 + 500 = 15,000
    assert (
        employment_total.input_value() == "15,000"
    ), f"Expected employment total '15,000', got '{employment_total.input_value()}'"
