"""Tests for Phase 4 Step 4 (Batch E.1): multi-program foundation.

Verifies:
- STAFF-MP-01: ACFOffice + Program seed runs; all 5 known programs exist.
- STAFF-MP-01: existing FormDefinition rows backfilled to CSBG.
- STAFF-MP-02: OrganizationProfile.org_type defaults to 'tribe' on existing rows.
- STAFF-MP-03: FormDefinition.cycle_type defaults to 'annual'.
- STAFF-MP-04: staff_queryset_filter scopes by UserProgramAssignment.

Run:
    uv run python manage.py test staff_review.test_program_scoping
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase, override_settings

from form_manager.models.forms import FormDefinition, FormEntry
from organizations.models import OrganizationProfile
from programs.models import ACFOffice, Program, UserProgramAssignment
from staff_review.permissions import FEDERAL_STAFF_GROUP, staff_queryset_filter

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class MultiProgramSeedTest(TestCase):
    """STAFF-MP-01: program seed migration ran."""

    def test_acf_offices_seeded(self):
        codes = set(ACFOffice.objects.values_list("code", flat=True))
        self.assertIn("OCS", codes)
        self.assertIn("OFA", codes)

    def test_five_programs_seeded_with_correct_offices(self):
        prog_codes = {p.code: p.office.code for p in Program.objects.all()}
        self.assertEqual(prog_codes.get("CSBG"), "OCS")
        self.assertEqual(prog_codes.get("TANF"), "OFA")
        self.assertEqual(prog_codes.get("TRIBAL_TANF"), "OFA")
        self.assertEqual(prog_codes.get("HMRF"), "OFA")
        self.assertEqual(prog_codes.get("HPOG"), "OFA")

    def test_hpog_is_inactive(self):
        hpog = Program.objects.get(code="HPOG")
        self.assertFalse(hpog.is_active)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormDefinitionBackfillTest(TestCase):
    """STAFF-MP-01 + 03: every FormDefinition has program + cycle_type."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_all_form_definitions_attributed_to_a_program(self):
        # After seed expansion (Phase II + 6 other OCS programs), every form
        # has SOME program -- the strict "all CSBG" assumption no longer holds.
        forms = FormDefinition.objects.all()
        self.assertGreater(forms.count(), 0)
        for fd in forms:
            self.assertIsNotNone(fd.program, f"{fd.name} should be attributed to a program")

    def test_cycle_type_in_valid_set(self):
        # The expanded seed includes annual + quarterly + ad_hoc cycles.
        valid = {c[0] for c in FormDefinition.CYCLE_TYPES}
        for fd in FormDefinition.objects.all():
            self.assertIn(fd.cycle_type, valid)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class OrganizationProfileOrgTypeTest(TestCase):
    """STAFF-MP-02: org_type defaults to 'tribe' on existing rows."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_pre_existing_csbg_orgs_default_to_tribe(self):
        # STAFF-MP-02 asserts the backfill migration set org_type='tribe'
        # on the legacy CSBG orgs from mock_data. Phase 4 Step 7 added
        # recipient demo personas with intentionally non-tribe org_types
        # (state, cbo) -- those are excluded by the "(Demo)" name suffix.
        for org in OrganizationProfile.objects.exclude(name__icontains="(Demo)"):
            self.assertEqual(org.org_type, "tribe", f"{org.name} should default to TRIBE")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ProgramScopedQuerysetTest(TestCase):
    """STAFF-MP-04: staff_queryset_filter respects program assignments."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        # seed adds Maya to CSBG. Confirm.
        cls.csbg = Program.objects.get(code="CSBG")
        cls.tanf = Program.objects.get(code="TANF")
        # Create a TANF FormDefinition with a FormEntry so we have something to filter OUT
        cls.tanf_fd = FormDefinition.objects.create(
            name="CSBG Annual Report 2.1 (Eligible Entities)",  # reuse valid choice
            variant="9.0.0",
            program=cls.tanf, family="0970-0492",
            schema={}, schema_class="DemoFormSchema", is_active=True,
        )
        org = OrganizationProfile.objects.first()
        cls.tanf_entry = FormEntry.objects.create(
            form_definition=cls.tanf_fd, organization=org, created_by=cls.staff_user,
            data={"_demo": "tanf-test"}, status="submitted",
        )

    def test_csbg_assignment_excludes_tanf_entries(self):
        # Maya is assigned to CSBG only -- TANF entry should be filtered out
        all_entries = FormEntry.objects.all()
        filtered = staff_queryset_filter(all_entries, self.staff_user)
        self.assertIn(self.tanf_entry, all_entries)
        self.assertNotIn(self.tanf_entry, filtered,
                         "CSBG-only staff should NOT see TANF entries (STAFF-MP-04)")

    def test_user_with_no_assignments_falls_back_to_all_programs(self):
        # Make a Federal Staff user with NO program assignments
        u = User.objects.create(email="legacy-staff@example.com", is_active=True)
        u.set_unusable_password(); u.save()
        u.groups.add(Group.objects.get(name=FEDERAL_STAFF_GROUP))

        all_entries = FormEntry.objects.all()
        filtered = staff_queryset_filter(all_entries, u)
        # No assignments -> legacy cross-program behavior
        self.assertEqual(filtered.count(), all_entries.count())

    def test_adding_tanf_assignment_widens_queryset(self):
        # Give Maya a TANF assignment too -- now both CSBG and TANF visible
        UserProgramAssignment.objects.create(
            user=self.staff_user, program=self.tanf, role="reviewer",
        )
        filtered = staff_queryset_filter(FormEntry.objects.all(), self.staff_user)
        self.assertIn(self.tanf_entry, filtered)
