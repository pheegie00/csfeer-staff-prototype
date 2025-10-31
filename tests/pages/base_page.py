"""
Base Page Object Model class for all pages.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str) -> None:
        """
        Initialize the page object.

        Args:
            page: Playwright page instance
            base_url: Base URL of the application
        """
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> None:
        """
        Navigate to a specific path.

        Args:
            path: Path to navigate to (relative to base_url)
        """
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def wait_for_url(self, pattern: str, timeout: int = 30000) -> None:
        """
        Wait for URL to match a pattern.

        Args:
            pattern: URL pattern to match
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_url(pattern, timeout=timeout)

    def click(self, selector: str) -> None:
        """
        Click an element.

        Args:
            selector: CSS selector or text selector
        """
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        """
        Fill an input field.

        Args:
            selector: CSS selector
            value: Value to fill
        """
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        """
        Get text content of an element.

        Args:
            selector: CSS selector

        Returns:
            Text content of the element
        """
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str) -> bool:
        """
        Check if an element is visible.

        Args:
            selector: CSS selector

        Returns:
            True if visible, False otherwise
        """
        return self.page.is_visible(selector)

    def expect_visible(self, selector: str) -> None:
        """
        Assert that an element is visible.

        Args:
            selector: CSS selector
        """
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        """
        Assert that an element contains text.

        Args:
            selector: CSS selector
            text: Expected text
        """
        expect(self.page.locator(selector)).to_contain_text(text)

    def screenshot(self, path: str) -> None:
        """
        Take a screenshot.

        Args:
            path: Path to save screenshot
        """
        self.page.screenshot(path=path)
