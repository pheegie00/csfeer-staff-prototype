"""
Page Object Model for login and authentication flows.
"""

import os
from urllib.parse import urlencode

from playwright.sync_api import Page, expect

from tests.e2e.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for login and authentication."""

    USER_MENU_SELECTOR = "button.usa-nav__link[aria-controls='agent-nav-section']"

    def __init__(self, page: Page, base_url: str) -> None:
        """Initialize the login page."""
        super().__init__(page, base_url)
        self.oauth_url = os.getenv("OAUTH_URL", "http://oauth.csfeer:8081")

    def navigate_to_login(self) -> None:
        """Navigate to login page via the login link."""
        self.navigate("/")
        login_link = self.page.get_by_role("link", name="Sign In")
        if login_link.is_visible():
            login_link.click()
            self.wait_for_oauth_page()

    def wait_for_oauth_page(self) -> None:
        """Wait for the OAuth/Keycloak login page to load."""
        self.page.wait_for_url(f"{self.oauth_url}/**")

    def login(self, username: str, password: str, expect_success: bool = True) -> None:
        """
        Perform login with credentials.

        Args:
            username: Username or email
            password: Password
            expect_success: Whether to expect successful login (default True)
        """
        self.navigate_to_login()

        # Fill username - use input field directly
        username_field = self.page.locator("input#username")
        username_field.fill(username)

        # Fill password - use input field directly to avoid "Show password" button
        password_field = self.page.locator("input#password[type='password']")
        password_field.fill(password)

        # Click sign in button
        sign_in_button = self.page.get_by_role("button", name="Sign In")
        sign_in_button.click()

        # Wait for redirect back to app only if expecting success
        if expect_success:
            self.page.wait_for_url(f"{self.base_url}/**")

    def logout(self) -> None:
        """Perform logout."""
        # Click the user menu button to expand submenu
        user_menu_button = self.page.locator(self.USER_MENU_SELECTOR)
        user_menu_button.click()

        # Wait for Sign Out link to become visible
        logout_link = self.page.get_by_role("link", name="Sign Out")
        logout_link.wait_for(state="visible", timeout=5000)
        logout_link.click()

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.

        Returns:
            True if logged in, False otherwise
        """
        # Check for user navigation menu presence (indicates logged in)
        user_nav = self.page.locator("nav.user-nav")
        return user_nav.is_visible()

    def expect_logged_in(self) -> None:
        """Assert that user is logged in."""
        # Check that user navigation menu is visible
        user_menu = self.page.locator("nav.user-nav")
        expect(user_menu).to_be_visible()

    def expect_logged_out(self) -> None:
        """Assert that user is logged out."""
        # After logout, user should be redirected and user nav should not be visible
        user_nav = self.page.locator("nav.user-nav")
        expect(user_nav).not_to_be_visible()

    def expect_login_error(self) -> None:
        """Assert that login error is displayed."""
        error = self.page.get_by_text("Invalid username or password")
        expect(error).to_be_visible()

    def navigate_with_login_error(
        self, source: str, error: str, description: str | None = None
    ) -> None:
        """Navigate to the home page with login error query params."""
        params: dict[str, str] = {"login_error_source": source, "login_error": error}
        if description:
            params["login_error_description"] = description
        self.navigate(f"/?{urlencode(params)}")

    def expect_okta_error(self) -> None:
        """Assert the Okta access-denied error alert is visible."""
        alert = self.page.locator(".usa-alert--error")
        expect(alert).to_be_visible()
        expect(alert.locator(".usa-alert__heading")).to_have_text("We couldn't sign you in.")

    def expect_no_org_error(self) -> None:
        """Assert the account-not-set-up warning alert is visible."""
        alert = self.page.locator(".usa-alert--warning")
        expect(alert).to_be_visible()
        expect(alert.locator(".usa-alert__heading")).to_have_text("You're not yet set up in CORE.")
