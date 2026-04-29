"""
End-to-end tests for the permissions scheme on the Tribal Short Form.

Role capabilities under test:
  - recipient-viewer   : form_view only — can view in-progress forms, nothing else
  - recipient-editor   : form_view + form_start + form_edit — no submit
  - recipient-approver : all editor permissions + form_submit
  - recipient-ao       : all approver permissions + tribal-plan AO signing
"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.fixtures.users import login_as

FORM_HEADING = "CSBG Annual Report 3.0 Tribal Short Form (Tribes)"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _start_tribal_short_form(page: Page, base_url: str) -> str:
    """Click 'Start New Form' on the Tribal Short Form card.

    Returns the base entry path, e.g. /forms/entry/<uuid>/.
    """
    page.goto(f"{base_url}/forms/")
    page.wait_for_load_state("networkidle")

    form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
    for i in range(form_cards.count()):
        card = form_cards.nth(i)
        if "Tribal Short Form" in card.inner_text():
            card.get_by_role("link", name="Start New Form").click()
            break

    page.get_by_role("heading", name="Your basic information").wait_for()

    match = re.search(r"/forms/entry/[^/?]+/", page.url)
    assert match, f"Could not extract entry path from URL: {page.url}"
    return match.group(0)


def _fill_section_1(page: Page) -> None:
    """Fill the minimum required fields on Section 1 (Basic Information)."""
    page.get_by_label("Name of Tribe or Tribal Organization *").fill("Permission Test Tribe")
    page.get_by_label("Full name *").fill("Permission Tester")
    page.get_by_label("Title *").fill("Director")
    page.get_by_label("Primary phone number *").fill("555-000-1111")
    page.get_by_label("Email address *").fill("permtest@example.org")


def _complete_and_submit(page: Page, base_url: str) -> None:
    """Complete the full Tribal Short Form workflow and submit it."""
    _start_tribal_short_form(page, base_url)
    _fill_section_1(page)

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Next →").click()
    page.get_by_text("Select all that apply:").wait_for()

    page.evaluate(
        """
        () => {
            const employment = document.querySelector('input[type="checkbox"][value*="employment"]');
            if (employment) {
                const label = document.querySelector(`label[for="${employment.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Expenditure amounts
    page.get_by_label("Employment *").fill("100000.00")
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Administration costs — select No
    page.evaluate(
        """
        () => {
            const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
            const noRadio = radios.find(r => {
                const label = document.querySelector(`label[for="${r.id}"]`);
                return label && label.textContent.trim() === 'No';
            });
            if (noRadio) {
                const label = document.querySelector(`label[for="${noRadio.id}"]`);
                if (label) label.click();
            }
        }
    """
    )
    page.wait_for_timeout(1000)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Expenditure details — employment description
    page.get_by_label("Description *").fill("Permission test: employment services description.")
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    with page.expect_navigation(timeout=5000):
        page.get_by_role("button", name="Next →").click()
    page.wait_for_timeout(1000)

    # Review and Submit
    assert "Review and Submit" in page.evaluate("() => document.body.innerText")
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    with page.expect_navigation(timeout=10000):
        page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)


# ---------------------------------------------------------------------------
# Fixture: create an in-progress form visible to the viewer, using the test's
# own page so no separate browser context is needed.  Logs in as recipient-ao
# (same org as the viewer), creates the form, saves and exits, then logs out.
# ---------------------------------------------------------------------------


@pytest.fixture
def viewer_form_path(page: Page, base_url: str) -> str:
    """Return the entry path of a freshly-created in-progress Tribal Short Form.

    Uses recipient-ao (same organisation as recipient-viewer) so the viewer
    can see the form.  Logs out afterward so the test can log in as viewer.
    """
    from tests.e2e.pages.login_page import LoginPage

    login_as(page, base_url, "recipient-ao")
    entry_path = _start_tribal_short_form(page, base_url)
    _fill_section_1(page)

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Save & Exit").click()
    page.wait_for_timeout(500)

    LoginPage(page, base_url).logout()

    return entry_path


# ---------------------------------------------------------------------------
# Viewer
# ---------------------------------------------------------------------------


class TestRecipientViewerPermissions:
    """recipient-viewer has form_view only."""

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_viewer_sees_form_list(self, page: Page, base_url: str) -> None:
        """Viewer can reach the form list."""
        login_as(page, base_url, "recipient-viewer")
        page.goto(f"{base_url}/forms/")
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("heading", name=FORM_HEADING)).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_viewer_cannot_start_form(self, page: Page, base_url: str) -> None:
        """'Start New Form' must not appear on the Tribal Short Form card for a viewer."""
        login_as(page, base_url, "recipient-viewer")
        page.goto(f"{base_url}/forms/")
        page.wait_for_load_state("networkidle")

        form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
        for i in range(form_cards.count()):
            card = form_cards.nth(i)
            if "Tribal Short Form" in card.inner_text():
                expect(card.get_by_role("link", name="Start New Form")).not_to_be_visible()
                return

        pytest.fail("Tribal Short Form card not found on the form list page")

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_viewer_can_access_preview_url(
        self, page: Page, base_url: str, viewer_form_path: str
    ) -> None:
        """Viewer navigating to the preview URL sees the preview page (not a redirect or 403)."""
        login_as(page, base_url, "recipient-viewer")
        page.goto(f"{base_url}{viewer_form_path}preview/")
        page.wait_for_load_state("networkidle")
        assert "preview" in page.url, f"Expected to stay on preview URL, got: {page.url}"
        expect(page.get_by_text("This is a read-only preview.")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_viewer_redirected_from_edit_url(
        self, page: Page, base_url: str, viewer_form_path: str
    ) -> None:
        """Viewer navigating directly to the edit URL must be redirected away.

        NOTE: This test is EXPECTED TO FAIL until a GET-level permission check is added
        to form_manager/views/form_edit.py. The POST is already guarded; the GET is not.
        """
        login_as(page, base_url, "recipient-viewer")
        page.goto(f"{base_url}{viewer_form_path}edit/")
        page.wait_for_load_state("networkidle")

        assert (
            "edit" not in page.url
        ), f"Viewer should be redirected away from the edit URL, but landed on: {page.url}"

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_viewer_cannot_submit(self, page: Page, base_url: str, viewer_form_path: str) -> None:
        """The preview page (the only page a viewer can reach) has no Submit button."""
        login_as(page, base_url, "recipient-viewer")
        page.goto(f"{base_url}{viewer_form_path}preview/")
        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        expect(page.get_by_role("button", name="Submit")).not_to_be_visible()


# ---------------------------------------------------------------------------
# Editor
# ---------------------------------------------------------------------------


class TestRecipientEditorPermissions:
    """recipient-editor has form_view, form_start, form_edit — no form_submit."""

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_editor_can_start_form(self, page: Page, base_url: str) -> None:
        """Editor can click 'Start New Form' and reach Section 1."""
        login_as(page, base_url, "recipient-editor")
        page.goto(f"{base_url}/forms/")
        page.wait_for_load_state("networkidle")

        form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
        for i in range(form_cards.count()):
            card = form_cards.nth(i)
            if "Tribal Short Form" in card.inner_text():
                card.get_by_role("link", name="Start New Form").click()
                break

        expect(page.get_by_role("heading", name="Your basic information")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_editor_can_fill_and_navigate(self, page: Page, base_url: str) -> None:
        """Editor can fill Section 1 and advance to Section 2."""
        login_as(page, base_url, "recipient-editor")
        _start_tribal_short_form(page, base_url)
        _fill_section_1(page)

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Next →").click()
        page.wait_for_load_state("networkidle")

        assert "step=1" in page.url, f"Expected step=1 in URL, got: {page.url}"

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_editor_can_save_and_exit(self, page: Page, base_url: str) -> None:
        """Editor can save a form and return to the form list."""
        login_as(page, base_url, "recipient-editor")
        _start_tribal_short_form(page, base_url)
        _fill_section_1(page)

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Save & Exit").click()
        page.wait_for_url(f"{base_url}/forms/")

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_editor_submit_button_disabled(self, page: Page, base_url: str) -> None:
        """Submit button is present but disabled for an editor on the review step."""
        login_as(page, base_url, "recipient-editor")
        entry_path = _start_tribal_short_form(page, base_url)
        _fill_section_1(page)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Save & Exit").click()
        page.wait_for_load_state("networkidle")

        page.goto(f"{base_url}{entry_path}edit/")
        page.wait_for_load_state("networkidle")
        side_nav = page.locator('nav[aria-label="Form sections"]')
        side_nav.get_by_text("Review and Submit").click()
        page.wait_for_load_state("networkidle")

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        submit_btn = page.get_by_role("button", name="Submit")
        expect(submit_btn).to_be_visible()
        expect(submit_btn).to_be_disabled()


# ---------------------------------------------------------------------------
# Approver
# ---------------------------------------------------------------------------


class TestRecipientApproverPermissions:
    """recipient-approver has form_view, form_start, form_edit, form_submit."""

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_approver_can_start_form(self, page: Page, base_url: str) -> None:
        """Approver can start a new Tribal Short Form."""
        login_as(page, base_url, "recipient-approver")
        page.goto(f"{base_url}/forms/")
        page.wait_for_load_state("networkidle")

        form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
        for i in range(form_cards.count()):
            card = form_cards.nth(i)
            if "Tribal Short Form" in card.inner_text():
                card.get_by_role("link", name="Start New Form").click()
                break

        expect(page.get_by_role("heading", name="Your basic information")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_approver_can_edit_form(self, page: Page, base_url: str) -> None:
        """Approver can fill fields and advance through sections."""
        login_as(page, base_url, "recipient-approver")
        _start_tribal_short_form(page, base_url)
        _fill_section_1(page)

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Next →").click()
        page.wait_for_load_state("networkidle")

        assert "step=1" in page.url, f"Expected step=1 in URL, got: {page.url}"

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_approver_submit_button_enabled(self, page: Page, base_url: str) -> None:
        """Submit button is enabled for an approver on the review step."""
        login_as(page, base_url, "recipient-approver")
        entry_path = _start_tribal_short_form(page, base_url)
        _fill_section_1(page)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Save & Exit").click()
        page.wait_for_load_state("networkidle")

        page.goto(f"{base_url}{entry_path}edit/")
        page.wait_for_load_state("networkidle")
        side_nav = page.locator('nav[aria-label="Form sections"]')
        side_nav.get_by_text("Review and Submit").click()
        page.wait_for_load_state("networkidle")

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        submit_btn = page.get_by_role("button", name="Submit")
        expect(submit_btn).to_be_visible()
        expect(submit_btn).to_be_enabled()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_approver_can_submit_form(self, page: Page, base_url: str) -> None:
        """Approver can complete and submit the Tribal Short Form."""
        login_as(page, base_url, "recipient-approver")
        _complete_and_submit(page, base_url)

        assert "Submitted at:" in page.evaluate("() => document.body.innerText")


# ---------------------------------------------------------------------------
# Authorized Official (AO)
# ---------------------------------------------------------------------------


class TestRecipientAOPermissions:
    """recipient-ao has all permissions (form_view, form_start, form_edit, form_submit)."""

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_ao_can_start_form(self, page: Page, base_url: str) -> None:
        """AO can start a new Tribal Short Form."""
        login_as(page, base_url, "recipient-ao")
        page.goto(f"{base_url}/forms/")
        page.wait_for_load_state("networkidle")

        form_cards = page.locator(".grid-col-12.tablet\\:grid-col-6")
        for i in range(form_cards.count()):
            card = form_cards.nth(i)
            if "Tribal Short Form" in card.inner_text():
                card.get_by_role("link", name="Start New Form").click()
                break

        expect(page.get_by_role("heading", name="Your basic information")).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_ao_can_edit_form(self, page: Page, base_url: str) -> None:
        """AO can fill fields and advance through sections."""
        login_as(page, base_url, "recipient-ao")
        _start_tribal_short_form(page, base_url)
        _fill_section_1(page)

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Next →").click()
        page.wait_for_load_state("networkidle")

        assert "step=1" in page.url, f"Expected step=1 in URL, got: {page.url}"

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_ao_submit_button_enabled(self, page: Page, base_url: str) -> None:
        """Submit button is enabled for an AO on the review step."""
        login_as(page, base_url, "recipient-ao")
        entry_path = _start_tribal_short_form(page, base_url)
        _fill_section_1(page)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Save & Exit").click()
        page.wait_for_load_state("networkidle")

        page.goto(f"{base_url}{entry_path}edit/")
        page.wait_for_load_state("networkidle")
        side_nav = page.locator('nav[aria-label="Form sections"]')
        side_nav.get_by_text("Review and Submit").click()
        page.wait_for_load_state("networkidle")

        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        submit_btn = page.get_by_role("button", name="Submit")
        expect(submit_btn).to_be_visible()
        expect(submit_btn).to_be_enabled()

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_ao_can_submit_form(self, page: Page, base_url: str) -> None:
        """AO can complete and submit the Tribal Short Form."""
        login_as(page, base_url, "recipient-ao")
        _complete_and_submit(page, base_url)

        assert "Submitted at:" in page.evaluate("() => document.body.innerText")
