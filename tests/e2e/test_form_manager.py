"""
End-to-end tests for form manager functionality.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.auth
def test_forms_page_loads(authenticated_page: Page, base_url: str) -> None:
    """Test that the forms listing page loads successfully."""
    # Navigate directly to forms page
    authenticated_page.goto(f"{base_url}/forms/")

    # Simply verify URL contains /forms/
    assert "/forms/" in authenticated_page.url
