"""Tests for Phase 4 Step 7: sample-user seed + View-as toggle.

Verifies:
- seed_demo_users command creates the 5 staff + 3 recipient personas
- Each staff persona has the right UserProgramAssignment(s)
- View-as POST: superuser can switch to a demo persona
- View-as POST: non-superuser gets 403
- View-as POST: switching to a non-allow-listed user is blocked
- DemoUsersIndexView is superuser-only
- The role_label context processor produces sensible strings
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from programs.models import Program, UserProgramAssignment
from staff_review.permissions import FEDERAL_STAFF_GROUP

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class SeedDemoUsersTest(TestCase):
    """seed_demo_users creates all 5 staff + 3 recipient personas."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_all_staff_personas_seeded(self):
        for email in [
            "maya.rodriguez@acf.hhs.gov",
            "dana.chen@acf.hhs.gov",
            "sam.patel@acf.hhs.gov",
            "riley.brooks@acf.hhs.gov",
            "root@acf.hhs.gov",
        ]:
            self.assertTrue(
                User.objects.filter(email=email).exists(),
                f"Expected staff persona {email} to be seeded",
            )

    def test_all_recipient_personas_seeded(self):
        for email in [
            "tribe-ao@example.com",
            "state-editor@example.com",
            "cbo-approver@example.com",
        ]:
            self.assertTrue(
                User.objects.filter(email=email).exists(),
                f"Expected recipient persona {email} to be seeded",
            )

    def test_ocs_admin_assigned_to_all_ocs_programs_only(self):
        dana = User.objects.get(email="dana.chen@acf.hhs.gov")
        assigned_offices = set(
            dana.program_assignments.values_list("program__office__code", flat=True)
        )
        self.assertEqual(assigned_offices, {"OCS"})
        # Dana's role on every CSBG/OCS program is 'admin'
        for a in dana.program_assignments.all():
            self.assertEqual(a.role, "admin")

    def test_ofa_admin_assigned_to_all_ofa_programs_only(self):
        sam = User.objects.get(email="sam.patel@acf.hhs.gov")
        assigned_offices = set(
            sam.program_assignments.values_list("program__office__code", flat=True)
        )
        self.assertEqual(assigned_offices, {"OFA"})
        # Sam covers TANF + Tribal TANF + HMRF + HPOG
        self.assertGreaterEqual(sam.program_assignments.count(), 3)
        for a in sam.program_assignments.all():
            self.assertEqual(a.role, "admin")

    def test_auditor_role_assigned(self):
        riley = User.objects.get(email="riley.brooks@acf.hhs.gov")
        for a in riley.program_assignments.all():
            self.assertEqual(a.role, "auditor")

    def test_superuser_has_is_superuser_flag(self):
        root = User.objects.get(email="root@acf.hhs.gov")
        self.assertTrue(root.is_superuser)
        # Superuser gets no UserProgramAssignment rows (they bypass via is_superuser)
        self.assertEqual(root.program_assignments.count(), 0)

    def test_idempotent_re_seed(self):
        before = User.objects.count()
        call_command("seed_demo_users", verbosity=0)
        after = User.objects.count()
        self.assertEqual(after, before, "Re-running seed should not create dupes")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ViewAsToggleTest(TestCase):
    """Phase 4 Step 7: View-as toggle is superuser-only + allow-listed."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.root = User.objects.get(email="root@acf.hhs.gov")
        cls.dana = User.objects.get(email="dana.chen@acf.hhs.gov")
        cls.sam = User.objects.get(email="sam.patel@acf.hhs.gov")
        cls.maya = User.objects.get(email="maya.rodriguez@acf.hhs.gov")

    def _client(self, user):
        c = Client(HTTP_HOST="localhost")
        c.force_login(user)
        return c

    def test_superuser_can_switch_to_demo_persona(self):
        c = self._client(self.root)
        resp = c.post(
            "/staff/demo-users/view-as/",
            data={"user_id": str(self.dana.id), "next": "/staff/"},
        )
        self.assertEqual(resp.status_code, 302)
        # Session should now identify as Dana (Django stores _auth_user_id).
        self.assertEqual(str(c.session["_auth_user_id"]), str(self.dana.id))

    def test_non_superuser_cannot_use_view_as(self):
        c = self._client(self.maya)  # Maya is staff but not superuser
        resp = c.post(
            "/staff/demo-users/view-as/",
            data={"user_id": str(self.dana.id)},
        )
        self.assertEqual(resp.status_code, 403)

    def test_view_as_rejects_non_allowlisted_user(self):
        # Create a NON-demo user (not in the seed_demo_users list)
        rando = User.objects.create(
            email="random@elsewhere.gov", is_active=True,
        )
        rando.set_unusable_password(); rando.save()

        c = self._client(self.root)
        resp = c.post(
            "/staff/demo-users/view-as/",
            data={"user_id": str(rando.id)},
        )
        self.assertEqual(resp.status_code, 403,
            "View-as should refuse to impersonate non-demo users")

    def test_demo_users_index_superuser_only(self):
        # Superuser sees the page
        c_root = self._client(self.root)
        resp = c_root.get("/staff/demo-users/")
        self.assertEqual(resp.status_code, 200)
        # Maya (non-superuser staff) gets 403
        c_maya = self._client(self.maya)
        resp2 = c_maya.get("/staff/demo-users/")
        self.assertEqual(resp2.status_code, 403)

    def test_demo_users_index_lists_all_seeded_personas(self):
        c = self._client(self.root)
        resp = c.get("/staff/demo-users/")
        # All 5 staff + 3 recipient emails should appear
        body = resp.content.decode()
        for email in [
            "maya.rodriguez@acf.hhs.gov", "dana.chen@acf.hhs.gov",
            "sam.patel@acf.hhs.gov", "riley.brooks@acf.hhs.gov",
            "root@acf.hhs.gov", "tribe-ao@example.com",
            "state-editor@example.com", "cbo-approver@example.com",
        ]:
            self.assertIn(email, body, f"{email} should appear in the personas list")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class RoleLabelTest(TestCase):
    """The staff_persona context processor produces sensible role labels."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def _role_label_for(self, email):
        from staff_review.context_processors import _role_label
        return _role_label(User.objects.get(email=email))

    def test_superuser_label(self):
        self.assertEqual(self._role_label_for("root@acf.hhs.gov"), "Platform Superuser")

    def test_ocs_admin_label(self):
        self.assertEqual(self._role_label_for("dana.chen@acf.hhs.gov"), "OCS Program Admin")

    def test_ofa_admin_label(self):
        self.assertEqual(self._role_label_for("sam.patel@acf.hhs.gov"), "OFA Program Admin")

    def test_auditor_label(self):
        self.assertEqual(self._role_label_for("riley.brooks@acf.hhs.gov"), "OCS Auditor")

    def test_reviewer_label(self):
        self.assertEqual(self._role_label_for("maya.rodriguez@acf.hhs.gov"), "OCS Reviewer")

    def test_recipient_ao_label(self):
        self.assertEqual(self._role_label_for("tribe-ao@example.com"), "Authorized Official")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class OFAFormsSeededTest(TestCase):
    """Phase 4 Step 7: OFA programs now have placeholder forms so an
    OFA admin sees a non-empty Form Builder view."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_tanf_has_forms(self):
        from form_manager.models.forms import FormDefinition
        self.assertTrue(
            FormDefinition.objects.filter(program__code="TANF").exists(),
            "TANF should have at least one seeded form",
        )

    def test_ofa_admin_form_builder_is_non_empty(self):
        sam = User.objects.get(email="sam.patel@acf.hhs.gov")
        c = Client(HTTP_HOST="localhost")
        c.force_login(sam)
        resp = c.get("/staff/form-builder/")
        self.assertEqual(resp.status_code, 200)
        owned = list(resp.context["owned_forms"])
        self.assertGreater(len(owned), 0, "OFA admin should see OFA forms")
        # All owned forms should be OFA
        for fd in owned:
            self.assertEqual(fd.program.office.code, "OFA")
