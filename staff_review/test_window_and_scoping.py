"""Tests for Batch F: SubmissionWindow (CORE-25) + FormScoping (CORE-22).

Run:
    uv run python manage.py test staff_review.test_window_and_scoping
"""

from datetime import datetime, timedelta, timezone as dt_tz

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from form_manager.models.forms import FormDefinition
from organizations.models import OrgType, OrganizationProfile, State
from programs.models import (
    FormScoping, Program, SubmissionWindow, SubmissionWindowStatus,
)

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m and "LoginRequiredMiddlewareWithCurrentPath" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class SubmissionWindowStatusTest(TestCase):
    """CORE-25: status derivation for Upcoming / Open / Past Due."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.csbg = Program.objects.get(code="CSBG")
        cls.form_def = FormDefinition.objects.filter(program=cls.csbg).first()

    def _make(self, opens_offset_days, closes_offset_days, fy="FY99"):
        now = timezone.now()
        return SubmissionWindow.objects.create(
            form_definition=self.form_def,
            fiscal_year=fy,
            opens_at=now + timedelta(days=opens_offset_days),
            closes_at=now + timedelta(days=closes_offset_days),
        )

    def test_upcoming_when_opens_in_future(self):
        w = self._make(opens_offset_days=7, closes_offset_days=30, fy="FY27")
        self.assertEqual(w.status, SubmissionWindowStatus.UPCOMING)
        self.assertTrue(w.is_upcoming)
        self.assertFalse(w.is_open)
        self.assertGreaterEqual(w.days_until_open, 6)

    def test_open_when_now_between_opens_and_closes(self):
        w = self._make(opens_offset_days=-7, closes_offset_days=7, fy="FY28")
        self.assertEqual(w.status, SubmissionWindowStatus.OPEN)
        self.assertTrue(w.is_open)
        self.assertGreaterEqual(w.days_until_close, 6)

    def test_past_due_when_closes_in_past(self):
        w = self._make(opens_offset_days=-30, closes_offset_days=-7, fy="FY24")
        self.assertEqual(w.status, SubmissionWindowStatus.PAST_DUE)
        self.assertTrue(w.is_past_due)
        self.assertLess(w.days_until_close, 0)

    def test_unique_per_form_per_fy(self):
        self._make(opens_offset_days=-7, closes_offset_days=7, fy="FY29")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            self._make(opens_offset_days=0, closes_offset_days=14, fy="FY29")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormScopingTest(TestCase):
    """CORE-22: rule-based + explicit-org form scoping."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.csbg = Program.objects.get(code="CSBG")
        # Pick the Tribal Plan specifically -- post-seed-expansion there are
        # multiple CSBG forms with different scopings; the tribal plan is the
        # one seeded with scope_to_org_types=["tribe"].
        cls.form_def = FormDefinition.objects.get(
            program=cls.csbg, name="CSBG Model Tribal Plan", variant="1.0.0",
        )
        cls.scoping = cls.form_def.scoping  # seeded with scope_to_org_types=["tribe"]

        state_ok = State.objects.get(code="OK")
        cls.tribe_org = OrganizationProfile.objects.filter(org_type=OrgType.TRIBE).first()
        cls.state_org = OrganizationProfile.objects.create(
            name="State of Oklahoma (Test)", state=state_ok, org_type=OrgType.STATE,
        )
        cls.cbo_org = OrganizationProfile.objects.create(
            name="Test CBO", state=state_ok, org_type=OrgType.CBO,
        )

    def test_rule_based_scope_includes_matching_type(self):
        self.assertTrue(self.scoping.is_org_in_scope(self.tribe_org))

    def test_rule_based_scope_excludes_non_matching_type(self):
        self.assertFalse(self.scoping.is_org_in_scope(self.state_org))
        self.assertFalse(self.scoping.is_org_in_scope(self.cbo_org))

    def test_explicit_org_adds_to_scope(self):
        # CBO not in scope by rule; add explicitly
        self.scoping.explicit_orgs.add(self.cbo_org)
        self.assertTrue(self.scoping.is_org_in_scope(self.cbo_org))

    def test_in_scope_org_count_counts_all(self):
        before = self.scoping.in_scope_org_count()
        self.scoping.explicit_orgs.add(self.cbo_org)
        after = self.scoping.in_scope_org_count()
        self.assertEqual(after, before + 1)

    def test_none_org_is_not_in_scope(self):
        self.assertFalse(self.scoping.is_org_in_scope(None))

    def test_validation_rejects_unknown_org_type(self):
        from django.core.exceptions import ValidationError
        scoping = FormScoping(
            form_definition=self.form_def, scope_to_org_types=["totally_made_up"],
        )
        with self.assertRaises(ValidationError):
            scoping.clean()


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormBuilderEditViewTest(TestCase):
    """Views: SubmissionWindowEditView + FormScopingEditView."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.csbg = Program.objects.get(code="CSBG")
        cls.form_def = FormDefinition.objects.filter(program=cls.csbg).first()

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        return c

    def test_window_edit_creates_new_fy(self):
        c = self._client()
        resp = c.post(f"/staff/form-builder/{self.form_def.id}/window/", data={
            "fiscal_year": "FY27",
            "opens_at": "2027-01-01",
            "closes_at": "2027-06-30",
        })
        self.assertEqual(resp.status_code, 302)
        w = SubmissionWindow.objects.get(form_definition=self.form_def, fiscal_year="FY27")
        self.assertEqual(w.opens_at.year, 2027)

    def test_window_edit_rejects_inverted_dates(self):
        c = self._client()
        existing = SubmissionWindow.objects.filter(form_definition=self.form_def).count()
        resp = c.post(f"/staff/form-builder/{self.form_def.id}/window/", data={
            "fiscal_year": "FY99",
            "opens_at": "2099-12-31",
            "closes_at": "2099-01-01",  # before opens
        })
        self.assertEqual(SubmissionWindow.objects.filter(form_definition=self.form_def).count(), existing)

    def test_window_edit_updates_existing_fy(self):
        c = self._client()
        c.post(f"/staff/form-builder/{self.form_def.id}/window/", data={
            "fiscal_year": "FY26",
            "opens_at": "2026-07-01",
            "closes_at": "2026-12-31",
        })
        w = SubmissionWindow.objects.get(form_definition=self.form_def, fiscal_year="FY26")
        self.assertEqual(w.opens_at.month, 7)

    def test_scope_edit_replaces_org_types(self):
        c = self._client()
        resp = c.post(f"/staff/form-builder/{self.form_def.id}/scope/", data={
            "org_types": ["state", "territory"],
        })
        self.assertEqual(resp.status_code, 302)
        self.form_def.refresh_from_db()
        scoping = self.form_def.scoping
        self.assertEqual(set(scoping.scope_to_org_types), {"state", "territory"})

    def test_scope_edit_filters_invalid_types(self):
        c = self._client()
        c.post(f"/staff/form-builder/{self.form_def.id}/scope/", data={
            "org_types": ["state", "made_up_type", "tribe"],
        })
        self.form_def.refresh_from_db()
        self.assertEqual(set(self.form_def.scoping.scope_to_org_types), {"state", "tribe"})
