"""
Test user fixtures and helpers.
"""

from typing import Generator

import pytest
from playwright.sync_api import Page

from tests.e2e.pages.login_page import LoginPage

# Test users from devops/mocks/keycloak/users.csv
TEST_USERS = {
    "admin": {
        "username": "admin",
        "password": "admin",
        "roles": ["csfeer_admin", "csfeer_user"],
    },
    "demo": {
        "username": "demo",
        "password": "demo",
        "roles": ["csfeer_user"],
    },
    "demo-1": {
        "username": "demo-1",
        "password": "demo-1",
        "roles": ["csfeer_user"],
    },
    "demo-2": {
        "username": "demo-2",
        "password": "demo-2",
        "roles": ["csfeer_user"],
    },
}


@pytest.fixture
def admin_page(page: Page, base_url: str) -> Generator[Page, None, None]:
    """
    Provide a page with an authenticated admin session.
    Admin user has both csfeer_admin and csfeer_user roles.
    """
    login_page = LoginPage(page, base_url)
    login_page.navigate_to_login()

    admin = TEST_USERS["admin"]
    login_page.login(admin["username"], admin["password"])

    yield page

    # Cleanup: logout after test
    try:
        login_page.logout()
    except Exception as e:
        print(f"Error during logout: {e}")


@pytest.fixture
def demo_page(page: Page, base_url: str) -> Generator[Page, None, None]:
    """
    Provide a page with an authenticated demo user session.
    Demo user has csfeer_user role.
    """
    login_page = LoginPage(page, base_url)
    login_page.navigate_to_login()

    demo = TEST_USERS["demo"]
    login_page.login(demo["username"], demo["password"])

    yield page

    # Cleanup: logout after test
    try:
        login_page.logout()
    except Exception:
        pass


def login_as(page: Page, base_url: str, username: str) -> None:
    """
    Helper function to login as a specific user.

    Args:
        page: Playwright page instance
        base_url: Base URL of the application
        username: Username from TEST_USERS
    """
    if username not in TEST_USERS:
        raise ValueError(f"Unknown user: {username}. Available: {list(TEST_USERS.keys())}")

    user = TEST_USERS[username]
    login_page = LoginPage(page, base_url)
    login_page.navigate_to_login()
    login_page.login(user["username"], user["password"])


def get_user_credentials(username: str) -> dict:
    """
    Get credentials for a test user.

    Args:
        username: Username from TEST_USERS

    Returns:
        Dictionary with username, password, and roles
    """
    if username not in TEST_USERS:
        raise ValueError(f"Unknown user: {username}. Available: {list(TEST_USERS.keys())}")

    return TEST_USERS[username].copy()
