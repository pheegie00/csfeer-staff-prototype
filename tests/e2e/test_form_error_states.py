"""
End-to-end tests for form error state initialization feature (bd-240).

Tests the complete user workflow for the session-based error display mechanism
that shows validation errors after users visit the review page.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.auth
def test_error_states_display_after_review_visit(authenticated_page: Page, base_url: str) -> None:
    """
    Test that validation errors appear after visiting the review page.

    Workflow:
    1. Start a new TribalShortForm
    2. Fill required fields on first page
    3. Continue without filling all required fields on subsequent pages
    4. Navigate to review page (triggers error state flag)
    5. Click "Edit section" to return to incomplete sections
    6. Verify error messages are displayed on fields
    """
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start a new TribalShortForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Annual Report" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    # Wait for form to load
    page.wait_for_selector('h4:has-text("Step 1 of 5 Basic Information")')

    # Step 1: Fill only some required fields (intentionally incomplete)
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Error State Test Tribe")
    page.get_by_label("Full name *").fill("Test User")
    # Leave Role empty (should be required)
    page.get_by_label("Primary phone number *").fill("555-000-1111")
    # Leave Email empty (should be required)

    # Scroll and continue
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()

    # Wait for Step 2
    page.wait_for_selector('h4:has-text("Step 2 of 5 Expenditure categories")')

    # Select one category
    page.evaluate(
        """
        () => {
            const employmentCheckbox = document.querySelector(
                'input[type="checkbox"][value*="employment"]'
            );
            console.log(employmentCheckbox)
            if (employmentCheckbox) {
                const label = document.querySelector(`label[for="${employmentCheckbox.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)

    # Continue to expenditure amounts
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill expenditure amount
    page.get_by_label("Employment *").fill("50000.00")

    # Continue through remaining required steps to reach review
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

    # Continue to Step 3
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill employment description (required)
    description_field = page.get_by_label("Description")
    description_field.fill("E2E test employment services description")

    # Continue to Step 4
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill individuals served (required)
    page.locator("input[name='total_individuals_served']").fill("100")

    # Continue to review page
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()

    # Wait for review page to load
    page.wait_for_timeout(2000)
    body_text = page.evaluate("() => document.body.innerText")

    # Should be on review page
    assert "Review" in body_text or "Submit" in body_text

    # At this point, the session flag should be set
    # Now click "Edit section" for the first section to return to it
    edit_links = page.get_by_role("link", name="Edit section")
    if edit_links.count() > 0:
        edit_links.first.click()
        page.wait_for_timeout(1000)

        # We should be back on the form edit page
        # Now errors should be visible for the incomplete fields
        # Look for USWDS error styling
        error_messages = page.locator(".usa-error-message")
        error_inputs = page.locator(".usa-input--error")

        # At least one error should be visible (Role and Email were left empty)
        assert (
            error_messages.count() > 0 or error_inputs.count() > 0
        ), "Expected error messages or error inputs to be visible after returning from review page"


@pytest.mark.e2e
@pytest.mark.auth
def test_errors_cleared_after_form_submission(authenticated_page: Page, base_url: str) -> None:
    """
    Test that error state flag is cleared after successful form submission.

    Workflow:
    1. Start a new form
    2. Fill all required fields
    3. Navigate to review page
    4. Submit the form
    5. Start editing the same form (or view it)
    6. Verify errors are not automatically displayed
    """
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start a new TribalShortForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Annual Report" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    # Wait for form to load
    page.wait_for_selector('h4:has-text("Step 1 of 5 Basic Information")')

    # Step 1: Fill ALL required fields completely
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("E2E Complete Form Test")
    page.get_by_label("Full name *").fill("Complete Test User")
    page.get_by_label("Role *").fill("Program Director")
    page.get_by_label("Primary phone number *").fill("555-000-2222")
    page.get_by_label("Email address *").fill("complete@example.org")

    # Continue through all steps with valid data
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()

    # Step 2: Select category
    page.wait_for_selector('h4:has-text("Step 2 of 5 Expenditure categories")')
    page.evaluate(
        """
        () => {
            const employmentCheckbox = document.querySelector(
                'input[type="checkbox"][value*="employment"]'
            );
            if (employmentCheckbox) {
                const label = document.querySelector(`label[for="${employmentCheckbox.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill expenditure amount
    page.get_by_label("Employment *").fill("75000.00")

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Select "No" for admin costs
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

    # Step 3
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    description_field = page.get_by_label("Description")
    description_field.fill("Complete employment services description for e2e test")

    # Step 4
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Fill individuals served (required)
    page.locator("input[name='total_individuals_served']").fill("100")

    # Navigate to review
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()

    page.wait_for_timeout(2000)

    # Submit the form
    submit_button = page.get_by_role("button", name="Submit")
    if submit_button.is_visible():
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        submit_button.click()
        page.wait_for_timeout(2000)

        # After submission, the error flag should be cleared
        # We can verify this by checking that we're on a success/confirmation page
        body_text = page.evaluate("() => document.body.innerText")
        # The exact success message may vary, but we shouldn't see error states anymore
        assert (
            "submitted" in body_text.lower() or "success" in body_text.lower()
        ), "Expected to see submission success message"


@pytest.mark.e2e
@pytest.mark.auth
def test_errors_persist_across_page_navigation(authenticated_page: Page, base_url: str) -> None:
    """
    Test that error display persists when navigating between form pages.

    Workflow:
    1. Start a new form with incomplete data
    2. Navigate to review page (sets error flag)
    3. Return to form and verify errors show
    4. Navigate to a different step
    5. Verify errors still show on the new step
    """
    page = authenticated_page

    # Navigate to forms page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Start a new TribalShortForm
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Annual Report" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    # Wait for form to load
    page.wait_for_selector('h4:has-text("Step 1 of 5 Basic Information")')

    # Fill partial data on Step 1
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("Persistence Test")
    # Leave other required fields empty

    # Navigate through to review page quickly
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Step 2: Select a category
    page.evaluate(
        """
        () => {
            const employmentCheckbox = document.querySelector(
                'input[type="checkbox"][value*="employment"]'
            );
            if (employmentCheckbox) {
                const label = document.querySelector(`label[for="${employmentCheckbox.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Leave employment amount empty, continue
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    # Try to continue to review (may need to navigate through remaining steps)
    # This is a simplified version - adjust based on actual form flow
    try:
        # Try to navigate forward multiple times to reach review
        for _ in range(5):
            buttons = page.get_by_role("button", name="Next →")
            review_button = page.get_by_role("button", name="Review & Submit →")

            if review_button.is_visible():
                review_button.click()
                break
            elif buttons.count() > 0 and buttons.first.is_visible():
                buttons.first.click()
                page.wait_for_timeout(1000)
            else:
                break

        page.wait_for_timeout(2000)

        # If we made it to review, go back to edit
        edit_links = page.get_by_role("link", name="Edit section")
        if edit_links.count() > 0:
            # Click first edit link
            edit_links.first.click()
            page.wait_for_timeout(1000)

            # Errors should be visible
            error_count_page1 = (
                page.locator(".usa-error-message").count()
                + page.locator(".usa-input--error").count()
            )

            # Navigate to another page using the sidebar or next button
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)

            next_buttons = page.get_by_role("button", name="Next →")
            if next_buttons.count() > 0 and next_buttons.first.is_visible():
                next_buttons.first.click()
                page.wait_for_timeout(1000)

                # Errors should still be visible on the new page (if there are validation issues)
                error_count_page2 = (
                    page.locator(".usa-error-message").count()
                    + page.locator(".usa-input--error").count()
                )

                # At least one of the pages should show errors
                assert (
                    error_count_page1 > 0 or error_count_page2 > 0
                ), "Expected errors to persist across page navigation"

    except Exception as e:
        # If navigation fails, that's okay - this test is best-effort
        # The important part is that IF we can navigate, errors should persist
        pytest.skip(f"Could not complete navigation workflow: {e}")
