"""End-to-end tests for Phase 4 Step 1: Return + Determination flows.

Verifies CORE-43, CORE-44, CORE-45, CORE-168, CORE-169, CORE-170.

Run:
    uv run python manage.py test staff_review.test_return_and_determination
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from form_manager.models.forms import FormAuditTrail, FormEntry
from staff_review.management.commands.seed_demo_data import stable_uuid
from staff_review.models import FormReturn, FormReturnItem

User = get_user_model()

_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m and "LoginRequiredMiddlewareWithCurrentPath" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ReturnFlowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.s1_id = stable_uuid("form_entry", "s1")  # Cherokee Nation, Submitted, has AO

    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")
        self.client.force_login(self.staff_user)

    def _post_return(self, sub_id, items=None, summary=""):
        """Helper -- POST a return with N items + optional summary."""
        items = items or [{"section": "Section 2", "field": "Phone", "text": "Phone number outdated."}]
        data = {"summary": summary}
        for i, it in enumerate(items, start=1):
            data[f"item-{i}-section"] = it["section"]
            data[f"item-{i}-field"] = it["field"]
            data[f"item-{i}-text"] = it["text"]
        return self.client.post(f"/staff/sub/{sub_id}/return/send/", data=data)

    # ----- CORE-168 -----

    def test_return_creates_form_return_with_items(self):
        resp = self._post_return("s1", items=[
            {"section": "Section 2", "field": "Phone", "text": "Phone outdated"},
            {"section": "Section 5", "field": "Admin", "text": "Admin too high"},
        ], summary="Two items to address.")
        self.assertEqual(resp.status_code, 302)

        entry = FormEntry.objects.get(id=self.s1_id)
        rets = entry.staff_returns.all()
        self.assertEqual(rets.count(), 1)
        ret = rets.first()
        self.assertEqual(ret.summary, "Two items to address.")
        self.assertEqual(ret.returned_by, self.staff_user)
        self.assertEqual(ret.items.count(), 2)
        self.assertEqual(ret.items.first().order, 1)
        self.assertEqual(ret.items.last().order, 2)

    def test_return_requires_at_least_one_item(self):
        resp = self.client.post(f"/staff/sub/s1/return/send/", data={"summary": "x"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(FormEntry.objects.get(id=self.s1_id).staff_returns.count(), 0)

    # ----- CORE-169 -----

    def test_one_return_limit_enforced(self):
        self._post_return("s1")
        self.assertEqual(FormEntry.objects.get(id=self.s1_id).staff_returns.count(), 1)
        # Second attempt should fail
        resp = self._post_return("s1", items=[{"section": "S2", "field": "F", "text": "Again"}])
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(FormEntry.objects.get(id=self.s1_id).staff_returns.count(), 1)

    # ----- CORE-43 -----

    def test_ao_signature_cleared_on_return(self):
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertTrue(entry.data["ao"].get("signed"), "AO should start signed")

        self._post_return("s1")

        entry.refresh_from_db()
        self.assertFalse(entry.data["ao"]["signed"])
        self.assertTrue(entry.data["ao"]["cleared"])
        self.assertTrue(entry.data["ao"]["clearedAt"])
        ret = entry.staff_returns.first()
        self.assertTrue(ret.ao_signature_cleared)

    # ----- CORE-170 -----

    def test_original_submission_snapshot_preserved(self):
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertNotIn("__original", entry.data)
        original_contact_name = entry.data["contact"]["name"]

        self._post_return("s1")

        entry.refresh_from_db()
        self.assertIn("__original", entry.data, "Snapshot key should be present")
        self.assertEqual(entry.data["__original"]["contact"]["name"], original_contact_name)

    # ----- status transition + audit -----

    def test_status_transitions_to_returned_and_audited(self):
        self._post_return("s1")
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertEqual(entry.status, "returned")
        self.assertTrue(FormAuditTrail.objects.filter(form_entry=entry, action="return").exists())


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class DeterminationFlowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.s1_id = stable_uuid("form_entry", "s1")
        cls.s4_id = stable_uuid("form_entry", "s4")  # Tanana Chiefs, Accepted (already resolved)

    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")
        self.client.force_login(self.staff_user)

    # ----- CORE-44 -----

    def test_accept_writes_determination(self):
        resp = self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Accepted", "notes": "All items addressed on resubmit."},
        )
        self.assertEqual(resp.status_code, 302)

        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertEqual(entry.determination_outcome, "accepted")
        self.assertEqual(entry.determination_notes, "All items addressed on resubmit.")
        self.assertEqual(entry.determined_by, self.staff_user)
        self.assertIsNotNone(entry.determined_at)
        self.assertEqual(entry.status, "accepted")

    def test_close_writes_determination_with_required_notes(self):
        resp = self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Closed", "notes": "Withdrew per recipient request."},
        )
        self.assertEqual(resp.status_code, 302)

        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertEqual(entry.determination_outcome, "closed")
        self.assertEqual(entry.status, "closed")

    def test_close_blocks_without_notes(self):
        resp = self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Closed", "notes": ""},
        )
        self.assertEqual(resp.status_code, 302)
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertIsNone(entry.determination_outcome)

    def test_invalid_outcome_rejected(self):
        resp = self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Maybe", "notes": "x"},
        )
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertIsNone(entry.determination_outcome)

    # ----- CORE-45 -----

    def test_determination_locks_submission(self):
        entry_before = FormEntry.objects.get(id=self.s1_id)
        self.assertFalse(entry_before.locked)

        self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Accepted", "notes": ""},
        )

        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertTrue(entry.locked)

    def test_already_resolved_cannot_be_re_determined(self):
        # s4 is already Accepted from seed
        entry = FormEntry.objects.get(id=self.s4_id)
        self.assertEqual(entry.status, "accepted")
        original_notes = entry.determination_notes

        resp = self.client.post(
            f"/staff/sub/s4/determination/record/",
            data={"outcome": "Closed", "notes": "Try to override"},
        )

        entry.refresh_from_db()
        # Determination did not change
        self.assertEqual(entry.determination_outcome, "accepted")
        self.assertEqual(entry.determination_notes, original_notes)

    def test_determination_writes_audit_trail(self):
        self.client.post(
            "/staff/sub/s1/determination/record/",
            data={"outcome": "Accepted", "notes": "ok"},
        )
        entry = FormEntry.objects.get(id=self.s1_id)
        self.assertTrue(FormAuditTrail.objects.filter(form_entry=entry, action="accept").exists())
