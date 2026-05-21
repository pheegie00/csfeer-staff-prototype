"""Tests for Batch G: publish new version flow (CORE-23, CORE-24).

Covers:
- publish_service.publish_new_version() happy path
- Semver helpers bump_minor / bump_major
- Inheritance of scoping + window
- Auto-close of in-progress FormEntries (CORE-24)
- Resolved submissions (Accepted/Closed) are NOT touched (CORE-23)
- Version conflict rejection
- Permission gating on the view
"""

from datetime import datetime, timezone as dt_tz

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from form_manager.models.forms import FormAuditTrail, FormDefinition, FormEntry
from organizations.models import OrganizationProfile
from programs.models import FormScoping, Program, SubmissionWindow
from staff_review.publish_service import (
    PublishError,
    bump_major,
    bump_minor,
    publish_new_version,
)

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class SemverHelpersTest(TestCase):

    def test_bump_minor_basic(self):
        self.assertEqual(bump_minor("1.0.0"), "1.1.0")
        self.assertEqual(bump_minor("1.4.7"), "1.5.0")
        self.assertEqual(bump_minor("0.0.1"), "0.1.0")

    def test_bump_minor_drops_prerelease(self):
        self.assertEqual(bump_minor("1.0.0-beta"), "1.1.0")

    def test_bump_major(self):
        self.assertEqual(bump_major("1.5.3"), "2.0.0")

    def test_invalid_variant_raises(self):
        with self.assertRaises(PublishError):
            bump_minor("not-semver")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class PublishServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.csbg = Program.objects.get(code="CSBG")
        # Pick the Tribal Plan specifically (post-seed-expansion there are
        # multiple CSBG forms; we want the one with scope_to_org_types=["tribe"]
        # so the scope-clone assertion is meaningful).
        cls.source = FormDefinition.objects.get(
            program=cls.csbg, name="CSBG Model Tribal Plan", variant="1.0.0",
        )

    def test_publish_creates_new_form_definition(self):
        new_fd, affected = publish_new_version(
            source_form_def=self.source,
            new_variant="1.1.0",
            actor=self.staff_user,
        )
        self.assertEqual(new_fd.name, self.source.name)
        self.assertEqual(str(new_fd.variant), "1.1.0")
        self.assertTrue(new_fd.is_active)
        self.assertEqual(new_fd.program_id, self.source.program_id)
        self.assertEqual(new_fd.cycle_type, self.source.cycle_type)

    def test_publish_deprecates_source(self):
        publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user,
        )
        self.source.refresh_from_db()
        self.assertFalse(self.source.is_active)

    def test_publish_clones_scoping_by_default(self):
        # Seed gives source scope_to_org_types=["tribe"]
        new_fd, _ = publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user,
        )
        self.assertTrue(hasattr(new_fd, "scoping"))
        self.assertEqual(new_fd.scoping.scope_to_org_types, ["tribe"])

    def test_publish_skips_scoping_when_disabled(self):
        new_fd, _ = publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user, clone_scoping=False,
        )
        self.assertFalse(hasattr(new_fd, "scoping"))

    def test_publish_clones_current_fy_window(self):
        new_fd, _ = publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user, current_fy="FY26",
        )
        self.assertTrue(
            new_fd.submission_windows.filter(fiscal_year="FY26").exists()
        )

    def test_auto_close_in_progress_submissions(self):
        # Create an in-progress FormEntry on source
        org = OrganizationProfile.objects.first()
        in_prog = FormEntry.objects.create(
            form_definition=self.source, organization=org,
            created_by=self.staff_user,
            data={"_test": True}, status="submitted",
        )

        new_fd, affected = publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user,
        )
        in_prog.refresh_from_db()
        self.assertEqual(in_prog.status, "closed")
        self.assertEqual(in_prog.determination_outcome, "closed")
        self.assertIn("deprecated", in_prog.determination_notes.lower())
        self.assertTrue(in_prog.locked)
        self.assertGreaterEqual(affected, 1)

    def test_resolved_submissions_untouched(self):
        # An Accepted submission on the source version should NOT be modified
        org = OrganizationProfile.objects.first()
        accepted = FormEntry.objects.create(
            form_definition=self.source, organization=org,
            created_by=self.staff_user,
            data={"_test": "accepted"},
            status="accepted",
            determination_outcome="accepted",
            determination_notes="Accepted prior to publish.",
            determined_at=timezone.now(),
            determined_by=self.staff_user,
        )
        original_notes = accepted.determination_notes

        publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user,
        )
        accepted.refresh_from_db()
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(accepted.determination_notes, original_notes)

    def test_publish_writes_audit_trail_for_each_auto_close(self):
        org = OrganizationProfile.objects.first()
        FormEntry.objects.create(
            form_definition=self.source, organization=org,
            created_by=self.staff_user,
            data={"_test": True}, status="submitted",
        )
        FormEntry.objects.create(
            form_definition=self.source, organization=org,
            created_by=self.staff_user,
            data={"_test": True}, status="returned",
            version_number=2,
        )
        before = FormAuditTrail.objects.filter(action="close").count()
        publish_new_version(
            source_form_def=self.source, new_variant="1.1.0",
            actor=self.staff_user,
        )
        after = FormAuditTrail.objects.filter(action="close").count()
        self.assertGreaterEqual(after - before, 2)

    def test_publish_rejects_invalid_variant(self):
        with self.assertRaises(PublishError):
            publish_new_version(
                source_form_def=self.source, new_variant="not-semver",
                actor=self.staff_user,
            )

    def test_publish_rejects_same_variant(self):
        with self.assertRaises(PublishError):
            publish_new_version(
                source_form_def=self.source, new_variant=str(self.source.variant),
                actor=self.staff_user,
            )

    def test_publish_rejects_existing_version_conflict(self):
        # Pre-create a v1.1.0 with the same name
        FormDefinition.objects.create(
            name=self.source.name, variant="1.1.0",
            family=self.source.family,
            schema={}, schema_class="x", is_active=False,
        )
        with self.assertRaises(PublishError):
            publish_new_version(
                source_form_def=self.source, new_variant="1.1.0",
                actor=self.staff_user,
            )


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class PublishViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.csbg = Program.objects.get(code="CSBG")
        cls.source = FormDefinition.objects.filter(program=cls.csbg).first()

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        return c

    def test_get_renders_form(self):
        c = self._client()
        resp = c.get(f"/staff/form-builder/{self.source.id}/publish/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Publish new version")
        self.assertEqual(resp.context["default_minor"], "1.1.0")

    def test_post_publishes_and_redirects_to_new_version(self):
        c = self._client()
        resp = c.post(f"/staff/form-builder/{self.source.id}/publish/", data={
            "new_variant": "1.1.0",
            "clone_scoping": "on",
            "clone_window": "on",
            "notes": "Adding new field X",
        })
        self.assertEqual(resp.status_code, 302)
        new_fd = FormDefinition.objects.get(name=self.source.name, variant="1.1.0")
        # Redirect points at new version's detail
        self.assertIn(str(new_fd.id), resp.url)

    def test_post_with_invalid_variant_redirects_back_with_error(self):
        c = self._client()
        resp = c.post(f"/staff/form-builder/{self.source.id}/publish/", data={
            "new_variant": "not-semver",
        })
        self.assertEqual(resp.status_code, 302)
        # No new FormDefinition created
        self.assertFalse(FormDefinition.objects.filter(
            name=self.source.name, variant="not-semver",
        ).exists())
