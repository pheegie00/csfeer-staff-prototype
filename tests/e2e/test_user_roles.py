"""
End-to-end tests for user roles and permissions.
"""

import pytest
from playwright.sync_api import Page

from tests.fixtures.users import get_user_credentials, login_as


@pytest.mark.e2e
@pytest.mark.auth
def test_admin_user_login(admin_page: Page, base_url: str) -> None:
    """Test that admin user can log in successfully."""
    page = admin_page

    # Admin should be logged in (from fixture)
    user_nav = page.locator("nav.user-nav")
    assert user_nav.is_visible(), "Admin user should be logged in"


@pytest.mark.e2e
@pytest.mark.auth
def test_demo_user_login(demo_page: Page, base_url: str) -> None:
    """Test that demo user can log in successfully."""
    page = demo_page

    # Demo user should be logged in (from fixture)
    user_nav = page.locator("nav.user-nav")
    assert user_nav.is_visible(), "Demo user should be logged in"


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(reason="Requires admin-only pages to be implemented")
def test_admin_can_access_admin_pages(admin_page: Page, base_url: str) -> None:
    """Test that admin user can access admin-only pages."""
    page = admin_page

    # Navigate to admin page
    page.goto(f"{base_url}/admin/")

    # Should not be redirected away
    page.wait_for_url(f"{base_url}/admin/**")


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.skip(reason="Requires role-based access control to be implemented")
def test_regular_user_cannot_access_admin_pages(demo_page: Page, base_url: str) -> None:
    """Test that regular users cannot access admin pages."""
    page = demo_page

    # Try to access admin page
    page.goto(f"{base_url}/admin/")

    # Should be redirected or show 403
    # Adjust assertion based on actual implementation
    assert page.url != f"{base_url}/admin/" or "403" in page.content()


@pytest.mark.e2e
@pytest.mark.auth
def test_login_with_different_users(page: Page, base_url: str) -> None:
    """Test that we can login with different test users."""
    # Test logging in as demo-1
    user1 = get_user_credentials("demo-1")
    login_as(page, base_url, "demo-1")

    user_nav = page.locator("nav.user-nav")
    assert user_nav.is_visible(), f"User {user1['username']} should be logged in"

    # Logout - expand menu and click Sign Out
    user_menu_button = page.locator("button.usa-nav__link[aria-controls='agent-nav-section']")
    user_menu_button.click()
    page.get_by_role("link", name="Sign Out").click()

    # Test logging in as demo-2
    user2 = get_user_credentials("demo-2")
    login_as(page, base_url, "demo-2")

    user_nav = page.locator("nav.user-nav")
    assert user_nav.is_visible(), f"User {user2['username']} should be logged in"
