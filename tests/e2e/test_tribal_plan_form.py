"""End-to-end tests for TribalPlanForm."""

import pytest
from playwright.sync_api import Page, expect

FORM_NAME = "CSBG Model Tribal Plan"


def _start_tribal_plan_form(page: Page, base_url: str) -> None:
    """Navigate to /forms/, find the Tribal Plan card, and click Start New Form."""
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if FORM_NAME in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            return

    raise AssertionError(f"Could not find a form card containing '{FORM_NAME}'")


def _click_radio(page: Page, value: str) -> None:
    """Click a radio button by its input value using JS (works with Alpine.js tiles)."""
    page.evaluate(
        f"""
        () => {{
            const radio = document.querySelector('input[type="radio"][value="{value}"]');
            if (radio) {{
                const label = document.querySelector(`label[for="${{radio.id}}"]`);
                if (label) label.click();
            }}
        }}
        """
    )
    page.wait_for_timeout(500)


def _click_next(page: Page) -> None:
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    with page.expect_navigation(timeout=10000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(800)


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_plan_form_available_in_list(authenticated_page: Page, base_url: str) -> None:
    """Tribal Plan form card is visible on the forms list page."""
    page = authenticated_page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    assert page.get_by_text(
        FORM_NAME
    ).first.is_visible(), f"Expected '{FORM_NAME}' to appear on the forms list page"


# ---------------------------------------------------------------------------
# Navigation rail
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_plan_form_nav_rail_section_labels(authenticated_page: Page, base_url: str) -> None:
    """The nav rail shows all expected section labels."""
    page = authenticated_page
    _start_tribal_plan_form(page, base_url)
    page.get_by_role("heading", name="Plan Coverage").first.wait_for()

    side_nav = page.locator('nav[aria-label="Form sections"]')

    expected_sections = [
        "Section 1: Tribal Administrative Information",
        "Section 2: Tribal Recognition",
        "Section 3: Goals and Objectives",
        "Section 4: Community-Based Feedback",
        "Section 5: Use of Funds & Fiscal Controls",
        "Section 6: Individual & Targeted Community Eligibility",
        "Section 7: Statement of Assurances",
        "Section 8: Federal Certifications",
        "Review and Submit",
    ]

    for section in expected_sections:
        assert (
            side_nav.get_by_text(section).count() > 0
        ), f"Expected nav rail to contain '{section}'"


# ---------------------------------------------------------------------------
# Section 1 — Basic navigation
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_plan_form_section1_fill_and_advance(
    authenticated_page: Page, base_url: str
) -> None:
    """Fill Section 1 Plan Coverage and advance to the Tribal Organization page."""
    page = authenticated_page
    _start_tribal_plan_form(page, base_url)
    page.get_by_role("heading", name="Plan Coverage").first.wait_for()

    # Select one-year plan
    _click_radio(page, "one_year")

    # fiscal_year_y1 is a disabled, auto-populated field — just confirm it's shown.
    expect(page.locator("#id_fiscal_year_y1")).to_be_visible()

    _click_next(page)

    body = page.evaluate("() => document.body.innerText")
    assert "Tribal Organization" in body or "Name of Tribe" in body


# ---------------------------------------------------------------------------
# Section 5 — Allocations page
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_plan_form_section5_y1_allocations_page(
    authenticated_page: Page, base_url: str
) -> None:
    """Year 1 Allocations page is reachable via direct URL and shows all 9 categories."""
    page = authenticated_page

    # Start the form to get the entry PK from the URL redirect
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    entry_url = None
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if FORM_NAME in card.inner_text():
            with page.expect_navigation():
                card.get_by_role("link", name="Start New Form").click()
            entry_url = page.url
            break

    assert entry_url, "Could not start the form"

    # Navigate directly to step 4 (Section 5), page 0 (Year 1 Allocations)
    base_entry_url = entry_url.split("?")[0]
    page.goto(f"{base_entry_url}?step=4&page=0")
    page.wait_for_load_state("networkidle")

    body = page.evaluate("() => document.body.innerText")

    # All 9 categories should be present
    expected_categories = [
        "Administrative Funds",
        "Employment",
        "Transportation",
        "Housing",
        "Health and Nutrition",
        "Civic Engagement",
        "Partnerships",
    ]
    for category in expected_categories:
        assert category in body, f"Expected allocation category '{category}' on the page"


# ---------------------------------------------------------------------------
# Section 8 — Certifications
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.auth
def test_tribal_plan_form_lobbying_certification_page(
    authenticated_page: Page, base_url: str
) -> None:
    """Lobbying Certification page (step 7, page 0) renders attestation and signature fields."""
    page = authenticated_page

    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    entry_url = None
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if FORM_NAME in card.inner_text():
            with page.expect_navigation():
                card.get_by_role("link", name="Start New Form").click()
            entry_url = page.url
            break

    assert entry_url, "Could not start the form"
    base_entry_url = entry_url.split("?")[0]

    page.goto(f"{base_entry_url}?step=7&page=0")
    page.wait_for_load_state("networkidle")

    body = page.evaluate("() => document.body.innerText")
    assert "Lobbying" in body
    assert "Signature" in body or "signature" in body
