"""
End-to-end tests for TribalShortForm functionality.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_short_form_complete_workflow(authenticated_page: Page, base_url: str) -> None:
    """Test complete workflow of TribalShortForm from start to submission."""
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Verify TribalShortForm is available
    short_form_heading = page.get_by_role(
        "heading", name="CSBG Annual Report 3.0 Tribal Short Form (Tribes)"
    )
    assert short_form_heading.is_visible(), "TribalShortForm should be available"

    # Click "Start New Form" for TribalShortForm
    # Find the card containing our form and click its Start New Form link
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    # Wait for form to load - should be on Step 1 of 4
    page.wait_for_selector('h4:has-text("Step 1 of 4 Basic Information")')

    # Step 1: Fill Basic Information
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Test Tribal Nation")
    page.get_by_label("Full name *").fill("E2E Test User")
    page.get_by_label("Title *").fill("Test Program Manager")
    page.get_by_label("Primary phone number *").fill("555-000-1111")
    page.get_by_label("Extension (Optional)").fill("1234")
    page.get_by_label("Email address *").fill("e2etest@example.org")
    page.get_by_label("Fax number (Optional)").fill("555-000-2222")

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Click Next
    page.get_by_role("button", name="Next →").click()

    # Wait for Step 2: Expenditure categories
    page.wait_for_selector('h4:has-text("Step 2 of 4 Expenditure categories")')

    # Verify Basic Information is marked completed
    assert page.locator('text="Basic Information" >> text="completed"').is_visible()

    # Select expenditure categories (Employment and Housing)
    # Wait for checkboxes to be visible
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

            if (employmentCheckbox) {
                const label = document.querySelector(`label[for="${employmentCheckbox.id}"]`);
                if (label) label.click();
            }

            if (housingCheckbox) {
                const label = document.querySelector(`label[for="${housingCheckbox.id}"]`);
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

    # Fill expenditure amounts
    page.get_by_label("Employment *").fill("80000.00")
    page.get_by_label("Housing *").fill("20000.00")

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to administration costs
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    assert "Administration costs" in page.evaluate("() => document.body.innerText")

    # Select "No" for administration costs (click the label)
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
    assert "3 of 4" in body_text
    assert "Expenditure details" in body_text

    # Verify Expenditure categories is marked completed
    assert page.locator('text="Expenditure categories" >> text="completed"').is_visible()

    # Fill employment services description
    page.get_by_label("Description *").fill(
        "E2E test: Employment services including job training and placement assistance."
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
        "E2E test: Housing assistance including emergency shelter and rental support."
    )

    # Scroll to bottom to show footer
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Continue to Step 4: Review and Submit
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)
    body_text = page.evaluate("() => document.body.innerText")
    assert "4 of 4" in body_text
    assert "Review and Submit" in body_text

    # Verify all sections are completed
    assert page.locator('text="Basic Information" >> text="completed"').is_visible()
    assert page.locator('text="Expenditure categories" >> text="completed"').is_visible()
    assert page.locator('text="Expenditure details" >> text="completed"').is_visible()

    # Verify data in review page
    assert page.get_by_text("E2E Test Tribal Nation").is_visible()
    assert page.get_by_text("E2E Test User").is_visible()
    assert page.get_by_text("80,000.00").is_visible()  # Employment amount
    assert page.get_by_text("20,000.00").is_visible()  # Housing amount
    assert page.get_by_text("100,000.00").is_visible()  # Total

    # Scroll to bottom to show footer before submission
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Submit the form
    with page.expect_navigation(timeout=10000):
        page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    body_text = page.evaluate("() => document.body.innerText")
    assert "Submitted at:" in body_text

    # Verify submission timestamp is present
    assert page.get_by_text("Submitted at:").is_visible()

    # Navigate back to forms list
    page.get_by_role("link", name="Back to List").click()
    page.wait_for_url(f"{base_url}/forms/")

    # Verify the form appears in the list with SUBMITTED status
    assert page.locator(
        'text="CSBG Annual Report 3.0 Tribal Short Form (Tribes)"'
    ).first.is_visible()
    assert page.locator('text="SUBMITTED"').first.is_visible()


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_short_form_has_four_steps(authenticated_page: Page, base_url: str) -> None:
    """Test that TribalShortForm has exactly 4 steps, not 5."""
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

    # Wait for form to load
    page.wait_for_selector('h4:has-text("Step 1 of 4")')

    # Verify step indicator shows 4 steps total
    step_indicator = page.locator('h4:has-text("Step 1 of 4")')
    assert step_indicator.is_visible(), "Should show Step 1 of 4"

    # Verify no demographic information in step list
    step_list = page.locator(".usa-step-indicator__segments")
    assert (
        step_list.get_by_text("Demographic information").count() == 0
    ), "Should NOT have demographic information step"

    # Count visible steps in the step indicator (should be 4)
    step_segments = page.locator(".usa-step-indicator__segment")
    step_count = step_segments.count()
    assert step_count == 4, f"Should have 4 steps, but found {step_count}"

    # Verify the step names in the step indicator
    steps = [
        "Basic Information",
        "Expenditure categories",
        "Expenditure details",
        "Review and Submit",
    ]

    for step_name in steps:
        step_in_indicator = step_list.locator(f"text={step_name}")
        assert step_in_indicator.count() > 0, f"Step '{step_name}' should be in step indicator"


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_short_form_vs_long_form_comparison(authenticated_page: Page, base_url: str) -> None:
    """Test that TribalShortForm and TribalLongForm are both available and different."""
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Verify both forms are available
    long_form = page.get_by_role(
        "heading", name="CSBG Annual Report 3.0 Tribal Annual Report (Tribes)"
    )
    short_form = page.get_by_role(
        "heading", name="CSBG Annual Report 3.0 Tribal Short Form (Tribes)"
    )

    assert long_form.is_visible(), "TribalLongForm should be available"
    assert short_form.is_visible(), "TribalShortForm should be available"

    # Start LongForm and verify it has 5 steps
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        card_text = card.inner_text()
        if "Tribal Annual Report" in card_text and "Short Form" not in card_text:
            card.get_by_role("link", name="Start New Form").click()
            break

    page.wait_for_selector('h4:has-text("Step 1 of 5")')
    assert page.locator('h4:has-text("Step 1 of 5")').is_visible(), "LongForm should have 5 steps"

    # Navigate back
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start ShortForm and verify it has 4 steps
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    page.wait_for_selector('h4:has-text("Step 1 of 4")')
    assert page.locator('h4:has-text("Step 1 of 4")').is_visible(), "ShortForm should have 4 steps"
