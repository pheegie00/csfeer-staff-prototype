"""
End-to-end tests for TribalLongForm functionality.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_long_form_complete_workflow(authenticated_page: Page, base_url: str) -> None:
    """Test complete 5-step workflow of TribalLongForm including demographic information."""
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Verify TribalLongForm is available
    long_form_heading = page.get_by_role(
        "heading", name="CSBG Annual Report 3.0 Tribal Annual Report (Tribes)"
    )
    assert long_form_heading.is_visible(), "TribalLongForm should be available"

    # Click "Start New Form" for TribalLongForm
    # Find all Start New Form links and click the one in the card with our form
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Annual Report" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    page.get_by_role("heading", name="Your basic information").wait_for()
    assert page.locator('nav[aria-label="Form sections"]').is_visible()
    assert page.locator(".usa-step-indicator").count() == 0

    # ==========================================
    # STEP 1: Basic Information
    # ==========================================
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Long Form Test Tribe")
    page.get_by_label("Full name *").fill("E2E Long Form Test User")
    page.get_by_label("Role *").fill("Test Program Director")
    page.get_by_label("Primary phone number *").fill("555-100-2222")
    page.get_by_label("Email address *").fill("e2elongform@example.org")

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Click Next
    page.get_by_role("button", name="Next →").click()

    page.get_by_text("Select all that apply:").wait_for()

    # ==========================================
    # STEP 2: Expenditure categories
    # ==========================================
    page.wait_for_selector('text="Select all that apply:"')

    # Click the checkbox labels (works with Alpine.js reactivity)
    page.evaluate(
        """
        () => {
            const employmentCheckbox = document.querySelector(
                'input[type="checkbox"][value*="employment"]'
            );
            const housingCheckbox = document.querySelector(
                'input[type="checkbox"][value*="housing"]'
            );
            const healthCheckbox = document.querySelector(
                'input[type="checkbox"][value*="health"]'
            );

            if (employmentCheckbox) {
                const label = document.querySelector(`label[for="${employmentCheckbox.id}"]`);
                if (label) label.click();
            }

            if (housingCheckbox) {
                const label = document.querySelector(`label[for="${housingCheckbox.id}"]`);
                if (label) label.click();
            }

            if (healthCheckbox) {
                const label = document.querySelector(`label[for="${healthCheckbox.id}"]`);
                if (label) label.click();
            }
        }
    """
    )

    # Wait for Alpine.js to process the changes
    page.wait_for_timeout(1000)

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to expenditure amounts
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Verify we're on the expenditure amounts page
    body_text = page.evaluate("() => document.body.innerText")
    assert "Provide the amounts" in body_text

    # Fill expenditure amounts (realistic distribution for a tribal program)
    # Total: $225,000 across three categories
    page.get_by_label("Employment *").fill("120000.00")
    page.get_by_label("Housing *").fill("75000.00")
    page.get_by_label("Health and Nutrition *").fill("30000.00")

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to administration costs
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    assert "Administration costs" in page.evaluate("() => document.body.innerText")

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

    # Wait for Alpine.js to process the changes
    page.wait_for_timeout(1000)

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to Step 3: Expenditure details
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText")
    assert "Expenditure details" in body_text

    # ==========================================
    # STEP 3: Expenditure details
    # ==========================================
    # Fill employment services description
    page.get_by_label("Description *").fill(
        "E2E test: Comprehensive employment services including job readiness training, "
        "resume workshops, interview preparation, and job placement assistance for tribal members."
    )

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to housing services description
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText.toLowerCase()")
    assert "housing" in body_text

    # Fill housing services description
    page.get_by_label("Description *").fill(
        "E2E test: Housing support including emergency shelter referrals, rental assistance, "
        "weatherization programs, and home repair services for low-income tribal households."
    )

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to health & nutrition services description
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText.toLowerCase()")
    assert "health" in body_text or "nutrition" in body_text

    # Fill health & nutrition services description
    page.get_by_label("Description *").fill(
        "E2E test: Health and nutrition services including nutrition education classes, "
        "food distribution programs, and health screening coordination for tribal members."
    )

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to Step 4: Demographic information
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText")
    assert "Demographic information" in body_text

    # ==========================================
    # STEP 4: Demographic information
    # Page 1: Total individuals and households
    # ==========================================
    # Realistic data: 150 individuals across 125 households (~1.2 people per household)
    # Note: Using .first and .nth(1) for duplicate "Total number of people" labels
    total_labels = page.get_by_label("Total number of people")
    total_labels.first.fill("150")  # Total individuals served

    households_label = page.get_by_label("Total number of people").nth(1)
    households_label.fill("125")  # Total households served

    # Wait for Alpine.js calculations
    page.wait_for_timeout(1500)

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to sex breakdown
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # STEP 4: Demographic information
    # Page 2: Sex breakdown
    # ==========================================
    # Sex distribution: 65 male, 60 female (total 125)
    # Note: Using name attributes to avoid label matching issues
    page.locator('input[name="male_individuals_served"]').fill("65")
    page.locator('input[name="female_individuals_served"]').fill("60")

    # Wait for Alpine.js to calculate total
    page.wait_for_timeout(1500)

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to employment status
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # STEP 4: Demographic information
    # Page 3: Employment status
    # ==========================================
    body_text = page.evaluate("() => document.body.innerText.toLowerCase()")
    assert "employment" in body_text or "employed" in body_text

    # Employment breakdown for 125 individuals (total matches sex breakdown)
    # Note: employment__retired field exists in schema but is NOT rendered on form
    page.locator('input[name="employment__full_time"]').fill("50")
    page.locator('input[name="employment__part_time"]').fill("25")
    page.locator('input[name="employment__migrant_seasonal"]').fill("0")
    page.locator('input[name="employment__unemployed_short_term"]').fill("18")
    page.locator('input[name="employment__unemployed_long_term"]').fill("15")
    page.locator('input[name="employment__permanently_unemployed"]').fill("10")
    page.locator('input[name="employment__unknown"]').fill("7")

    # Wait for Alpine.js to calculate total
    page.wait_for_timeout(1500)

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to Step 5: Review and Submit
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText")
    assert "Review and Submit" in body_text
    assert page.locator('nav[aria-label="Form sections"]').is_visible()
    assert page.locator(".usa-step-indicator").count() == 0

    # Verify basic information in review page
    assert page.get_by_text("E2E Long Form Test Tribe").is_visible()
    assert page.get_by_text("E2E Long Form Test User").is_visible()

    # Verify expenditure amounts in review page
    assert page.get_by_text("120,000.00").is_visible()  # Employment amount
    assert page.get_by_text("75,000.00").is_visible()  # Housing amount
    assert page.get_by_text("30,000.00").is_visible()  # Health & Nutrition amount
    assert page.get_by_text("225,000.00").is_visible()  # Total expenditures

    # Verify demographic data in review page
    # Total individuals and households
    assert page.get_by_text("150").first.is_visible()  # Total individuals served
    assert page.get_by_text("125").first.is_visible()  # Total households served

    # Sex breakdown
    assert page.get_by_text("65").first.is_visible()  # Male
    assert page.get_by_text("60").first.is_visible()  # Female

    # Employment status (spot check key values)
    assert page.get_by_text("50").first.is_visible()  # Employed Full Time
    assert page.get_by_text("25").first.is_visible()  # Employed Part Time
    assert page.get_by_text("18").first.is_visible()  # Unemployed short-term

    # Scroll to bottom to show footer before submission
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Submit the form
    with page.expect_navigation(timeout=10000):
        page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    body_text = page.evaluate("() => document.body.innerText")

    # Verify submission confirmation
    assert "Submitted at:" in body_text or "submitted" in body_text.lower()

    # Verify the form entry shows submitted status
    assert (
        "submitted" in body_text.lower() or "complete" in body_text.lower()
    ), "Form should show submitted/complete status"
