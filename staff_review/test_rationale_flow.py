"""End-to-end test for CORE-167 rationale wiring (Phase 3 Step 1).

Validates:
- seed_demo_data creates the expected DB rows
- POSTing to /staff/sub/<id>/save-edit/ stages pending edits in session
- POSTing to /staff/sub/<id>/rationale/ with a valid rationale:
    * creates FormAuditTrail(action='edit_on_behalf', rationale=...)
    * creates FormAuditDetail per changed field (old + new value)
    * applies the edits to FormEntry.data
    * transitions FormEntry.status from 'submitted' to 'amended'
- Empty rationale is rejected
- apply_db_overlay reflects DB-applied edits on the next detail render

Run:
    uv run python manage.py test staff_review.test_rationale_flow
"""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase

from form_manager.models.forms import FormAuditDetail, FormAuditTrail, FormEntry
from staff_review.management.commands.seed_demo_data import stable_uuid

User = get_user_model()


class RationaleFlowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Populate the demo data once per test class
        call_command("seed_demo_data", verbosity=0)
        cls.s1_id = stable_uuid("form_entry", "s1")
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.staff_user)

    def test_seed_creates_expected_rows(self):
        self.assertEqual(FormEntry.objects.count(), 9)
        e = FormEntry.objects.get(id=self.s1_id)
        self.assertEqual(e.status, "submitted")
        self.assertIn("Cherokee", e.organization.name)

    def test_save_edit_stages_pending(self):
        resp = self.client.post(
            "/staff/sub/s1/save-edit/",
            data={"contact.name": "Sarah Whitewater-Updated"},
        )
        self.assertEqual(resp.status_code, 302)
        # Re-fetch session via client
        self.assertEqual(
            self.client.session.get("pending_edits_s1", {}).get("contact.name", {}).get("value"),
            "Sarah Whitewater-Updated",
        )

    def test_rationale_required(self):
        # Stage an edit
        self.client.post(
            "/staff/sub/s1/save-edit/",
            data={"contact.name": "Sarah Whitewater-Updated"},
        )
        # Submit rationale with empty text
        resp = self.client.post(
            "/staff/sub/s1/rationale/",
            data={"rationale": "   "},
        )
        self.assertEqual(resp.status_code, 302)
        # No new audit trail row
        self.assertEqual(
            FormAuditTrail.objects.filter(form_entry_id=self.s1_id, action="edit_on_behalf").count(),
            0,
        )

    def test_rationale_writes_to_db_and_applies_edits(self):
        # Capture baseline
        before = FormEntry.objects.get(id=self.s1_id)
        original_contact_name = before.data["contact"]["name"]
        self.assertNotEqual(original_contact_name, "Sarah Whitewater-Updated")

        # Stage edit
        self.client.post(
            "/staff/sub/s1/save-edit/",
            data={"contact.name": "Sarah Whitewater-Updated"},
        )
        # Save with rationale
        resp = self.client.post(
            "/staff/sub/s1/rationale/",
            data={"rationale": "Updated per phone call with Sarah on 5/21"},
        )
        self.assertEqual(resp.status_code, 302)

        # FormEntry.data updated
        after = FormEntry.objects.get(id=self.s1_id)
        self.assertEqual(after.data["contact"]["name"], "Sarah Whitewater-Updated")

        # Status transitioned
        self.assertEqual(after.status, "amended")

        # Audit trail created
        trails = FormAuditTrail.objects.filter(form_entry=after, action="edit_on_behalf")
        self.assertEqual(trails.count(), 1)
        trail = trails.first()
        self.assertEqual(trail.rationale, "Updated per phone call with Sarah on 5/21")
        self.assertEqual(trail.user, self.staff_user)

        # FormAuditDetail row per changed field
        details = FormAuditDetail.objects.filter(form_entry=after, field_name="contact.name")
        self.assertEqual(details.count(), 1)
        detail = details.first()
        self.assertEqual(detail.old_value, original_contact_name)
        self.assertEqual(detail.new_value, "Sarah Whitewater-Updated")

        # Session pending cleared
        self.assertEqual(self.client.session.get("pending_edits_s1", {}), {})

    def test_detail_view_overlays_db_edits(self):
        # Apply an edit via the rationale flow
        self.client.post(
            "/staff/sub/s1/save-edit/",
            data={"contact.name": "Sarah Whitewater-Updated"},
        )
        self.client.post(
            "/staff/sub/s1/rationale/",
            data={"rationale": "Updated per phone call"},
        )

        # Visit detail page -- updated name should be visible (overlay applied)
        resp = self.client.get("/staff/sub/s1/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sarah Whitewater-Updated")
        # Status pill should reflect amended (mapped to "In Progress" in display)
        self.assertContains(resp, "In Progress")
