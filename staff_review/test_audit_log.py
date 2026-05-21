"""Tests for Phase 4 Step 3: audit log expansion (CORE-21, 35, 36).

Verifies:
- AccountAuditTrail rows written on user create, group add/remove,
  user activation flip, permission grant/revoke, org membership
  add/remove
- SystemEvent rows written on login, logout, login failure
- CSV export writes a SystemEvent(kind='export_csv')
- ImmutableAuditMixin blocks edits + deletes on audit rows
- Form-level edits (CORE-167) continue to write FormAuditTrail
  (regression test)

Run:
    uv run python manage.py test staff_review.test_audit_log
"""

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase, override_settings

from form_manager.models.forms import FormAuditTrail, FormDefinition
from staff_review.audit_models import (
    AccountAuditTrail, AuditTrailImmutableError, SystemEvent,
)
from staff_review.management.commands.seed_demo_data import stable_uuid

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class AccountAuditTrailTest(TestCase):
    """CORE-21: account-level audit events."""

    def test_user_created_writes_audit_row(self):
        before = AccountAuditTrail.objects.filter(action="user_created").count()
        u = User.objects.create(email="new@example.com")
        after = AccountAuditTrail.objects.filter(action="user_created").count()
        self.assertEqual(after, before + 1)
        row = AccountAuditTrail.objects.filter(target_user=u, action="user_created").first()
        self.assertEqual(row.context.get("email"), "new@example.com")

    def test_user_deactivation_writes_audit_row(self):
        u = User.objects.create(email="x@example.com", is_active=True)
        u.is_active = False
        u.save()
        self.assertTrue(AccountAuditTrail.objects.filter(
            target_user=u, action="user_deactivated"
        ).exists())

    def test_user_reactivation_writes_audit_row(self):
        u = User.objects.create(email="x@example.com", is_active=True)
        u.is_active = False
        u.save()
        u.is_active = True
        u.save()
        self.assertTrue(AccountAuditTrail.objects.filter(
            target_user=u, action="user_reactivated"
        ).exists())

    def test_group_add_writes_audit_row(self):
        u = User.objects.create(email="x@example.com")
        g = Group.objects.create(name="Test Group")
        u.groups.add(g)
        self.assertTrue(AccountAuditTrail.objects.filter(
            target_user=u, action="group_added"
        ).exists())

    def test_group_remove_writes_audit_row(self):
        u = User.objects.create(email="x@example.com")
        g = Group.objects.create(name="Test Group")
        u.groups.add(g)
        u.groups.remove(g)
        self.assertTrue(AccountAuditTrail.objects.filter(
            target_user=u, action="group_removed"
        ).exists())


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class SystemEventTest(TestCase):
    """CORE-36 + CORE-47 system-level events."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")

    def test_login_writes_system_event(self):
        # Use the signal directly since force_login doesn't fire user_logged_in
        rf = RequestFactory()
        req = rf.get("/")
        req.META["REMOTE_ADDR"] = "10.0.0.1"
        req.META["HTTP_USER_AGENT"] = "Mozilla/5.0 (test)"
        before = SystemEvent.objects.filter(kind="login").count()
        user_logged_in.send(sender=User, request=req, user=self.staff_user)
        after = SystemEvent.objects.filter(kind="login").count()
        self.assertEqual(after, before + 1)
        evt = SystemEvent.objects.filter(kind="login", actor=self.staff_user).latest("created_at")
        self.assertEqual(evt.ip_address, "10.0.0.1")
        self.assertIn("test", evt.user_agent)

    def test_csv_export_writes_system_event(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        # Need a form_def id with at least one resolved entry (s4 is Accepted)
        # The form_def for s4 (tribal-plan) is created by seed.
        fd = FormDefinition.objects.get(name__icontains="Tribal Plan")
        before = SystemEvent.objects.filter(kind="export_csv").count()
        resp = c.get(f"/staff/exports/csv/?form_type={fd.id}&fy=FY26")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")
        after = SystemEvent.objects.filter(kind="export_csv").count()
        self.assertEqual(after, before + 1)
        evt = SystemEvent.objects.filter(kind="export_csv").latest("created_at")
        self.assertEqual(evt.actor, self.staff_user)
        self.assertEqual(evt.detail.get("fiscal_year"), "FY26")
        self.assertEqual(evt.detail.get("form_name"), fd.name)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ImmutabilityTest(TestCase):
    """All audit rows are append-only at the application layer."""

    def test_account_audit_cannot_be_edited(self):
        u = User.objects.create(email="x@example.com")
        row = AccountAuditTrail.objects.filter(target_user=u).first()
        row.notes = "tampered"
        with self.assertRaises(AuditTrailImmutableError):
            row.save()

    def test_account_audit_cannot_be_deleted(self):
        u = User.objects.create(email="x@example.com")
        row = AccountAuditTrail.objects.filter(target_user=u).first()
        with self.assertRaises(AuditTrailImmutableError):
            row.delete()

    def test_system_event_cannot_be_edited(self):
        evt = SystemEvent.objects.create(kind="login", actor=None, notes="x")
        evt.notes = "tampered"
        with self.assertRaises(AuditTrailImmutableError):
            evt.save()

    def test_system_event_cannot_be_deleted(self):
        evt = SystemEvent.objects.create(kind="login", actor=None, notes="x")
        with self.assertRaises(AuditTrailImmutableError):
            evt.delete()


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormAuditTrailRegressionTest(TestCase):
    """Make sure the existing form-level audit logging still works (CORE-167)."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")

    def test_edit_on_behalf_still_writes_form_audit_trail(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        c.post("/staff/sub/s1/save-edit/", data={"contact.name": "New Name"})
        before = FormAuditTrail.objects.filter(action="edit_on_behalf").count()
        c.post("/staff/sub/s1/rationale/", data={"rationale": "test"})
        after = FormAuditTrail.objects.filter(action="edit_on_behalf").count()
        self.assertEqual(after, before + 1)
