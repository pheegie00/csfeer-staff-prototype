"""
Pytest configuration and fixtures for e2e tests.
"""

import os
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

# Import user fixtures
pytest_plugins = ["tests.fixtures.users"]

# Base URL for the application
BASE_URL = os.environ.get("BASE_URL", "http://ui.csfeer:8000")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Override browser context args for all tests.
    Adds common settings like viewport, locale, and timezone.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def base_url() -> str:
    """Provide base URL for the application."""
    return BASE_URL


@pytest.fixture
def context(
    browser: Browser,
    browser_context_args: dict,
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    """
    Create a new browser context for each test.
    Enables video recording and tracing for debugging.
    """
    context = browser.new_context(
        **browser_context_args,
        record_video_dir="tests/videos/",
        record_video_size={"width": 1920, "height": 1080},
    )

    # Start tracing for debugging
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Save trace with a unique filename per test
    test_name = request.node.name.replace("/", "_").replace("\\", "_")
    trace_path = f"tests/traces/trace_{test_name}.zip"
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture
def page(context: BrowserContext, base_url: str) -> Generator[Page, None, None]:
    """
    Create a new page in the context.
    Sets up the page with default timeout and base URL.
    """
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds
    page.set_default_navigation_timeout(30000)

    yield page

    page.close()


@pytest.fixture
def authenticated_page(page: Page, base_url: str) -> Generator[Page, None, None]:
    """
    Provide a page with an authenticated session.
    Uses Keycloak test user credentials.
    """
    from tests.e2e.pages.login_page import LoginPage

    # Navigate to the application
    page.goto(base_url)

    # Check if already logged in (nav.user-nav visible means authenticated)
    if page.locator("nav.user-nav").is_visible():
        yield page
        return

    # Use LoginPage to handle OAuth flow
    login_page = LoginPage(page, base_url)
    login_page.login("demo", "demo")

    # Verify logged in
    expect(page.locator("nav.user-nav")).to_be_visible()

    yield page


@pytest.fixture(autouse=True)
def setup_test_directories() -> None:
    """Ensure test output directories exist."""
    os.makedirs("tests/videos", exist_ok=True)
    os.makedirs("tests/traces", exist_ok=True)
    os.makedirs("tests/screenshots", exist_ok=True)


# Markers for pytest
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "e2e: end-to-end tests using Playwright")
    config.addinivalue_line("markers", "auth: tests that require authentication")
    config.addinivalue_line("markers", "slow: slow running tests")
