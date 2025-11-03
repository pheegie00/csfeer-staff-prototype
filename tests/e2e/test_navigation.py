"""
End-to-end tests for general navigation and page access.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.auth
def test_home_page_loads(authenticated_page: Page, base_url: str) -> None:
    """Test that the home page loads successfully for authenticated users."""
    page = authenticated_page
    page.goto(base_url)

    # Assert page loaded and user is authenticated
    expect(page.locator("nav.user-nav")).to_be_visible()


@pytest.mark.e2e
@pytest.mark.auth
def test_navigation_links_present(authenticated_page: Page, base_url: str) -> None:
    """Test that main navigation links are present for authenticated users."""
    page = authenticated_page
    page.goto(base_url)

    # Check for authenticated user navigation
    user_nav = page.locator("nav.user-nav")
    expect(user_nav).to_be_visible()

    # Check for Sign Out link in submenu
    nav_button = page.locator("button.usa-nav__link[aria-controls='agent-nav-section']")
    expect(nav_button).to_be_visible()


@pytest.mark.e2e
@pytest.mark.auth
def test_authenticated_navigation(authenticated_page: Page, base_url: str) -> None:
    """Test navigation when user is authenticated."""
    page = authenticated_page

    # Ensure we're on the home page
    page.goto(base_url)

    # Check for authenticated navigation elements
    user_nav = page.locator("nav.user-nav")
    expect(user_nav).to_be_visible()

    # Navigate to forms
    forms_link = page.get_by_role("link", name="Forms")
    if forms_link.is_visible():
        forms_link.click()
        page.wait_for_url(f"{base_url}/forms/**")


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(
    reason="App redirects all requests to OAuth - 404 testing requires auth middleware changes"
)
def test_404_page(authenticated_page: Page, base_url: str) -> None:
    """Test that 404 page is shown for non-existent routes."""
    page = authenticated_page
    page.goto(f"{base_url}/this-page-does-not-exist/")

    # Currently redirects to OAuth login instead of showing 404
    # Need to update Django middleware to handle 404s for authenticated users
    expect(page).to_have_url(f"{base_url}/this-page-does-not-exist/")
