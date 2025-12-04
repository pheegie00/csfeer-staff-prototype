"""
End-to-end tests for authentication flow.
"""

import pytest
from playwright.sync_api import Page

from tests.e2e.pages.login_page import LoginPage


@pytest.mark.e2e
@pytest.mark.auth
def test_user_can_login(page: Page, base_url: str) -> None:
    """Test that a user can successfully log in."""
    login_page = LoginPage(page, base_url)

    # Navigate to login
    login_page.navigate_to_login()

    # Perform login with test credentials
    login_page.login("demo", "demo")

    # Assert user is logged in
    login_page.expect_logged_in()


@pytest.mark.e2e
@pytest.mark.auth
def test_user_can_logout(page: Page, base_url: str) -> None:
    """Test that a logged-in user can log out."""
    login_page = LoginPage(page, base_url)

    # Login first
    login_page.navigate_to_login()
    login_page.login("demo", "demo")
    login_page.expect_logged_in()

    # Perform logout
    login_page.logout()

    # Assert user is logged out
    login_page.expect_logged_out()


@pytest.mark.e2e
@pytest.mark.auth
def test_login_with_invalid_credentials(page: Page, base_url: str) -> None:
    """Test that login fails with invalid credentials."""
    login_page = LoginPage(page, base_url)

    # Navigate to login
    login_page.navigate_to_login()

    # Try to login with invalid credentials (don't expect success)
    login_page.login("invalid_user", "wrong_password", expect_success=False)

    # Wait for error message to appear
    login_page.page.wait_for_selector("text=Invalid username or password")

    # Assert error message is shown
    login_page.expect_login_error()


@pytest.mark.e2e
@pytest.mark.auth
def test_protected_page_redirects_to_login(page: Page, base_url: str) -> None:
    """Test that accessing a protected page redirects to login."""
    # Try to access forms page without authentication
    page.goto(f"{base_url}/forms/")

    # Should be redirected to OAuth login
    page.wait_for_url("**/oauth.csfeer:8081/**")
