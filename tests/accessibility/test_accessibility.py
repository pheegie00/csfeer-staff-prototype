"""
Accessibility tests using axe-core via axe-playwright-python.

These are dev-only tests and are NOT run in CI. Run them manually during
development to catch WCAG 2.1 AA violations before they reach review.

Usage:
    uv run pytest tests/accessibility/ -v
"""

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.accessibility
def test_home_page_accessibility(demo_page: Page, base_url: str) -> None:
    """Home page has no axe-detectable accessibility violations."""
    demo_page.goto(base_url)
    demo_page.wait_for_load_state("networkidle")

    results = Axe().run(demo_page)
    assert results.violations_count == 0, results.generate_report()


@pytest.mark.e2e
@pytest.mark.accessibility
def test_tribal_short_form_step1_accessibility(demo_page: Page, base_url: str) -> None:
    """Tribal Short Form step 1 has no axe-detectable accessibility violations."""
    page = demo_page
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    # Navigate into the first step of the Tribal Short Form
    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    page.get_by_role("heading", name="Your basic information").wait_for()

    results = Axe().run(page)
    assert results.violations_count == 0, results.generate_report()
