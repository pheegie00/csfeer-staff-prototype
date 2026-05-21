"""Tests for Batch E.2: Form Builder UI program scoping.

Verifies:
- FormBuilderListView shows only the user's assigned-program forms
- Shared forms (is_shared=True) appear in a separate section visible to all
- Users assigned to multiple programs see all their forms
- FormBuilderDetailView renders + flags "can_manage" correctly
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from form_manager.constants import (
    CSBGAnnualReportForms,
    CSBGTribalPlanApplicationForms,
    FormFamilies,
)
from form_manager.models.forms import FormDefinition
from programs.models import Program, UserProgramAssignment
from staff_review.permissions import FEDERAL_STAFF_GROUP

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormBuilderProgramScopingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.csbg = Program.objects.get(code="CSBG")
        cls.tanf = Program.objects.get(code="TANF")

        # Add a TANF-scoped form (reusing a valid choice from constants)
        cls.tanf_form = FormDefinition.objects.create(
            name=CSBGAnnualReportForms.STATES_ANNUAL_REPORT_3_0.value,  # placeholder; valid choice
            variant="1.0.0",
            program=cls.tanf,
            family=FormFamilies.CSBG_ANNUAL_REPORT.value,
            schema={}, schema_class="TANFDemo", is_active=True,
            cycle_type="quarterly",
        )

        # A shared form (e.g., SF-424 stand-in)
        cls.shared_form = FormDefinition.objects.create(
            name=CSBGAnnualReportForms.ENTITITES_ANNUAL_REPORT_3_0.value,  # valid choice
            variant="1.0.0",
            family=FormFamilies.CSBG_ANNUAL_REPORT.value,
            schema={}, schema_class="SharedDemo", is_active=True,
            is_shared=True,
            program=None,
        )

    def _client(self, user):
        c = Client(HTTP_HOST="localhost")
        c.force_login(user)
        return c

    def test_csbg_user_sees_only_csbg_owned_forms(self):
        # Maya is assigned to CSBG only -- should NOT see TANF form in 'owned'
        c = self._client(self.staff_user)
        resp = c.get("/staff/form-builder/")
        self.assertEqual(resp.status_code, 200)
        owned_forms = resp.context["owned_forms"]
        for fd in owned_forms:
            self.assertEqual(
                fd.program.code, "CSBG",
                f"{fd.name} should be CSBG-scoped (Maya only manages CSBG)"
            )
        # TANF form should NOT appear in owned list
        self.assertNotIn(self.tanf_form, list(owned_forms))

    def test_shared_forms_visible_to_all_staff(self):
        c = self._client(self.staff_user)
        resp = c.get("/staff/form-builder/")
        shared = list(resp.context["shared_forms"])
        self.assertIn(self.shared_form, shared)

    def test_user_with_no_assignments_sees_no_owned_forms(self):
        u = User.objects.create(email="legacy@example.com", is_active=True)
        u.set_unusable_password(); u.save()
        u.groups.add(Group.objects.get(name=FEDERAL_STAFF_GROUP))
        c = self._client(u)
        resp = c.get("/staff/form-builder/")
        self.assertEqual(list(resp.context["owned_forms"]), [])
        # But shared forms still appear
        self.assertIn(self.shared_form, list(resp.context["shared_forms"]))

    def test_multi_program_user_sees_both(self):
        # Add TANF assignment to Maya -- now both CSBG and TANF forms visible
        UserProgramAssignment.objects.create(
            user=self.staff_user, program=self.tanf, role="reviewer",
        )
        c = self._client(self.staff_user)
        resp = c.get("/staff/form-builder/")
        owned = list(resp.context["owned_forms"])
        self.assertIn(self.tanf_form, owned)

    def test_detail_view_renders_for_user_program(self):
        # CSBG form -- Maya should be able to manage
        csbg_form = FormDefinition.objects.filter(program=self.csbg).first()
        c = self._client(self.staff_user)
        resp = c.get(f"/staff/form-builder/{csbg_form.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["can_manage"])

    def test_detail_view_for_unassigned_program_shows_no_manage(self):
        c = self._client(self.staff_user)
        resp = c.get(f"/staff/form-builder/{self.tanf_form.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["can_manage"])

    def test_shared_form_only_manageable_by_superuser(self):
        # Maya is a Federal Staff user but not superuser -- can't manage shared
        c = self._client(self.staff_user)
        resp = c.get(f"/staff/form-builder/{self.shared_form.id}/")
        self.assertFalse(resp.context["can_manage"])

        # Superuser can
        super_u = User.objects.create_superuser(email="root@example.com", password="x")
        c2 = self._client(super_u)
        resp2 = c2.get(f"/staff/form-builder/{self.shared_form.id}/")
        self.assertTrue(resp2.context["can_manage"])
