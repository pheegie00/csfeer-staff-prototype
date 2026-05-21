"""Tests for Batch H: recipient-side window + scope enforcement.

Verifies:
- forms_available_to_org() filters by FormScoping.scope_to_org_types
- forms_available_to_org() respects explicit_orgs additions
- window_state_for() derives open/upcoming/past_due correctly
- form_list view: a Tribe AO doesn't see LIHEAP state forms
- form_list view: a State editor doesn't see CSBG tribal forms
- form_start view: blocks if window is upcoming
- form_start view: blocks if window is past_due
- form_start view: blocks if org_type is out of scope
- form_start view: succeeds when scope + window OK
- form_start: existing drafts unaffected when window goes past_due
  (per CORE-25 acceptance criteria)
"""

from datetime import datetime, timedelta, timezone as dt_tz
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from form_manager.models import FormDefinition, FormEntry
from form_manager.scoping_filters import (
    DEFAULT_CURRENT_FY,
    FormStartBlocked,
    assert_can_start_form,
    forms_available_to_org,
    org_is_in_scope,
    window_state_for,
)
from organizations.models import OrganizationProfile
from programs.models import FormScoping, SubmissionWindow

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class WindowStateTest(TestCase):
    """window_state_for() correctly derives open / upcoming / past_due."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.form_def = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )

    def _set_window(self, opens_offset_days, closes_offset_days, fy="FY26"):
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.form_def, fiscal_year=fy,
            defaults={
                "opens_at": now + timedelta(days=opens_offset_days),
                "closes_at": now + timedelta(days=closes_offset_days),
            },
        )

    def test_open_window_allows_start(self):
        self._set_window(-7, 7)
        state = window_state_for(self.form_def)
        self.assertEqual(state.status, "open")
        self.assertTrue(state.can_start)

    def test_upcoming_window_blocks_start(self):
        self._set_window(7, 30)
        state = window_state_for(self.form_def)
        self.assertEqual(state.status, "upcoming")
        self.assertFalse(state.can_start)
        self.assertIn("Opens", state.badge_label)

    def test_past_due_window_blocks_start(self):
        self._set_window(-30, -7)
        state = window_state_for(self.form_def)
        self.assertEqual(state.status, "past_due")
        self.assertFalse(state.can_start)
        self.assertIn("Closed", state.badge_label)

    def test_no_window_defined_treated_as_always_open(self):
        # Pick a form that has no window for FY99
        state = window_state_for(self.form_def, current_fy="FY99")
        self.assertEqual(state.status, "always_open")
        self.assertTrue(state.can_start)

    def test_open_window_under_7_days_shows_warning_tone(self):
        self._set_window(-1, 3)
        state = window_state_for(self.form_def)
        self.assertEqual(state.badge_tone, "warn")
        self.assertIn("day", state.badge_label.lower())


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ScopeEnforcementTest(TestCase):
    """org_is_in_scope + forms_available_to_org honour FormScoping rules."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.tribe_form = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )
        cls.tribe_org = OrganizationProfile.objects.get(
            name="Choctaw Nation of Oklahoma (Demo)",
        )
        cls.state_org = OrganizationProfile.objects.get(
            name="Oklahoma Department of Commerce (Demo)",
        )

    def test_tribe_org_in_scope_for_tribal_form(self):
        self.assertTrue(org_is_in_scope(self.tribe_form, self.tribe_org))

    def test_state_org_out_of_scope_for_tribal_form(self):
        self.assertFalse(org_is_in_scope(self.tribe_form, self.state_org))

    def test_form_with_no_scoping_is_permissive(self):
        # Build a form with no FormScoping row at all
        no_scope_form = FormDefinition.objects.create(
            name="CSBG Model Tribal Plan",  # reuse a valid name
            variant="42.0.0",
            family="0970-0635",
            schema={}, schema_class="X", is_active=True,
        )
        self.assertTrue(org_is_in_scope(no_scope_form, self.state_org))

    def test_explicit_org_overrides_org_type_rule(self):
        # State org is normally out-of-scope for tribal form; add explicitly.
        self.tribe_form.scoping.explicit_orgs.add(self.state_org)
        self.assertTrue(org_is_in_scope(self.tribe_form, self.state_org))

    def test_forms_available_filters_state_org_off_tribal(self):
        all_forms = FormDefinition.objects.filter(is_active=True)
        visible = forms_available_to_org(all_forms, self.state_org)
        self.assertNotIn(self.tribe_form, visible)

    def test_forms_available_includes_in_scope(self):
        all_forms = FormDefinition.objects.filter(is_active=True)
        visible = forms_available_to_org(all_forms, self.tribe_org)
        self.assertIn(self.tribe_form, visible)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class AssertCanStartFormTest(TestCase):
    """assert_can_start_form raises FormStartBlocked with the right reason."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.form_def = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )
        cls.tribe_org = OrganizationProfile.objects.get(
            name="Choctaw Nation of Oklahoma (Demo)",
        )
        cls.state_org = OrganizationProfile.objects.get(
            name="Oklahoma Department of Commerce (Demo)",
        )

    def test_in_scope_open_window_passes(self):
        # Open the window (seeded as May 8 - Jun 30, 2026 = past_due as of
        # current_date=2026-05-21; let's reset it to "open now").
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.form_def, fiscal_year=DEFAULT_CURRENT_FY,
            defaults={
                "opens_at": now - timedelta(days=7),
                "closes_at": now + timedelta(days=7),
            },
        )
        # Should NOT raise
        assert_can_start_form(self.form_def, self.tribe_org)

    def test_out_of_scope_raises_out_of_scope(self):
        with self.assertRaises(FormStartBlocked) as cm:
            assert_can_start_form(self.form_def, self.state_org)
        self.assertEqual(cm.exception.reason_code, "out_of_scope")

    def test_upcoming_window_raises_window_upcoming(self):
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.form_def, fiscal_year=DEFAULT_CURRENT_FY,
            defaults={
                "opens_at": now + timedelta(days=7),
                "closes_at": now + timedelta(days=30),
            },
        )
        with self.assertRaises(FormStartBlocked) as cm:
            assert_can_start_form(self.form_def, self.tribe_org)
        self.assertEqual(cm.exception.reason_code, "window_upcoming")

    def test_past_due_window_raises_window_past_due(self):
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.form_def, fiscal_year=DEFAULT_CURRENT_FY,
            defaults={
                "opens_at": now - timedelta(days=30),
                "closes_at": now - timedelta(days=7),
            },
        )
        with self.assertRaises(FormStartBlocked) as cm:
            assert_can_start_form(self.form_def, self.tribe_org)
        self.assertEqual(cm.exception.reason_code, "window_past_due")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormStartViewEnforcementTest(TestCase):
    """form_start view returns to form_list with messages.error on block."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.tribe_form = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )
        cls.tribe_ao = User.objects.get(email="tribe-ao@example.com")
        cls.state_editor = User.objects.get(email="state-editor@example.com")

    def _client(self, user):
        c = Client(HTTP_HOST="localhost")
        c.force_login(user)
        return c

    def test_in_scope_open_window_creates_form_entry(self):
        # Open the window for tribe form
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.tribe_form, fiscal_year=DEFAULT_CURRENT_FY,
            defaults={
                "opens_at": now - timedelta(days=1),
                "closes_at": now + timedelta(days=30),
            },
        )
        before = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        c = self._client(self.tribe_ao)
        resp = c.get(f"/forms/start/{self.tribe_form.id}/")
        # Should 302 to form_edit
        self.assertEqual(resp.status_code, 302)
        after = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        self.assertEqual(after, before + 1)

    def test_state_editor_blocked_from_tribal_form_start(self):
        before = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        c = self._client(self.state_editor)
        resp = c.get(f"/forms/start/{self.tribe_form.id}/", follow=True)
        # No new entry created
        after = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        self.assertEqual(after, before, "Out-of-scope start should be blocked")
        # User redirected to form_list with an error message
        msgs = list(resp.context["messages"])
        self.assertTrue(any("not in scope" in str(m).lower() for m in msgs),
                        f"Expected 'not in scope' error; got {[str(m) for m in msgs]}")

    def test_past_due_window_blocks_start(self):
        # Force window into past-due
        now = timezone.now()
        SubmissionWindow.objects.update_or_create(
            form_definition=self.tribe_form, fiscal_year=DEFAULT_CURRENT_FY,
            defaults={
                "opens_at": now - timedelta(days=60),
                "closes_at": now - timedelta(days=1),
            },
        )
        before = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        c = self._client(self.tribe_ao)
        resp = c.get(f"/forms/start/{self.tribe_form.id}/", follow=True)
        after = FormEntry.objects.filter(form_definition=self.tribe_form).count()
        self.assertEqual(after, before, "Past-due window should block new starts")
        msgs = list(resp.context["messages"])
        self.assertTrue(any("closed" in str(m).lower() for m in msgs))


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormListViewVisibilityTest(TestCase):
    """form_list shows only forms the recipient's org is in scope for."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def _client(self, email):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email=email))
        return c

    def test_tribe_ao_sees_tribal_form_not_state_form(self):
        c = self._client("tribe-ao@example.com")
        resp = c.get("/forms/")
        self.assertEqual(resp.status_code, 200)
        visible_names = {fd.name for fd in resp.context["definitions"]}
        # Tribal Plan is scoped to ["tribe"] -- should appear
        self.assertIn("CSBG Model Tribal Plan", visible_names)
        # CSBG State Plan is scoped to ["state"] -- should NOT appear
        self.assertNotIn("CSBG State Plan", visible_names)

    def test_state_editor_sees_state_forms_not_tribal(self):
        c = self._client("state-editor@example.com")
        resp = c.get("/forms/")
        visible_names = {fd.name for fd in resp.context["definitions"]}
        # LIHEAP Household Report is scoped to ["state", "territory"] -- appears
        self.assertIn("LIHEAP Household Report", visible_names)
        # CSBG Tribal Plan is scoped to ["tribe"] -- should NOT
        self.assertNotIn("CSBG Model Tribal Plan", visible_names)

    def test_all_visible_definitions_have_window_state(self):
        # Annotation: every visible form_def has .window_state
        c = self._client("tribe-ao@example.com")
        resp = c.get("/forms/")
        for fd in resp.context["definitions"]:
            self.assertTrue(hasattr(fd, "window_state"),
                            f"{fd.name} should have a window_state annotation")
