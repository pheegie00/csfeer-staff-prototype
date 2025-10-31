"""
Page Object Model for form manager functionality.
"""

from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class FormManagerPage(BasePage):
    """Page object for form manager operations."""

    def __init__(self, page: Page, base_url: str) -> None:
        """Initialize the form manager page."""
        super().__init__(page, base_url)
        self.forms_path = "/forms/"

    def navigate_to_forms(self) -> None:
        """Navigate to forms listing page."""
        self.navigate(self.forms_path)

    def expect_on_forms_page(self) -> None:
        """Assert that we're on the forms page."""
        self.wait_for_url(f"{self.base_url}{self.forms_path}**")

    def get_form_count(self) -> int:
        """
        Get the number of forms displayed.

        Returns:
            Number of forms on the page
        """
        # Adjust selector based on actual implementation
        forms = self.page.locator("[data-testid='form-item']")
        return forms.count()

    def click_form(self, form_name: str) -> None:
        """
        Click on a form by its name.

        Args:
            form_name: Name of the form to click
        """
        form_link = self.page.get_by_role("link", name=form_name)
        form_link.click()

    def expect_form_visible(self, form_name: str) -> None:
        """
        Assert that a form is visible.

        Args:
            form_name: Name of the form
        """
        form_link = self.page.get_by_role("link", name=form_name)
        expect(form_link).to_be_visible()

    def fill_form_field(self, label: str, value: str) -> None:
        """
        Fill a form field by its label.

        Args:
            label: Label of the form field
            value: Value to fill
        """
        field = self.page.get_by_label(label)
        field.fill(value)

    def submit_form(self) -> None:
        """Submit the current form."""
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.click()

    def expect_success_message(self) -> None:
        """Assert that success message is displayed."""
        success = self.page.get_by_text("Form submitted successfully")
        expect(success).to_be_visible()

    def expect_error_message(self) -> None:
        """Assert that error message is displayed."""
        error = self.page.locator("[role='alert']")
        expect(error).to_be_visible()

    def expect_validation_error(self, field_label: str) -> None:
        """
        Assert that validation error is shown for a field.

        Args:
            field_label: Label of the field with error
        """
        field = self.page.get_by_label(field_label)
        # Look for error message near the field
        error = field.locator("xpath=following-sibling::*[contains(@class, 'error')]")
        expect(error).to_be_visible()
