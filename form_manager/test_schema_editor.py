"""Tests for the visual Form Builder schema editor (STAFF-MP-14).

Covers the pure schema-mutation functions and the draft lifecycle helpers,
and asserts that every mutation leaves the spec lint-clean.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from form_manager.models import FormDefinition
from form_manager.services import schema_editor as se
from form_manager.services.formspec_service import lint_definition, load_builtin_spec

User = get_user_model()
_TEST_MIDDLEWARE = [
    m for m in settings.MIDDLEWARE
    if "oauth2_authcodeflow" not in m and "LoginRequiredMiddlewareWithCurrentPath" not in m
]


class SchemaEditorPureTest(TestCase):
    """Pure-function tests -- no DB."""

    def setUp(self):
        self.spec = load_builtin_spec("csbg_tribal_plan")
        self.assertIsNotNone(self.spec)

    # ---- key + type helpers ------------------------------------------
    def test_slug_camelizes(self):
        self.assertEqual(se.slug("Annual goals"), "annualGoals")
        self.assertEqual(se.slug("  Mission   Statement "), "missionStatement")
        self.assertEqual(se.slug("!!!"), "field")

    def test_unique_key_disambiguates(self):
        # 'name' already exists in the org section.
        k = se.unique_key(self.spec, "name")
        self.assertNotIn(k, se.all_keys(self.spec))

    def test_field_type_roundtrip(self):
        for ft in se.FIELD_TYPES:
            built = se.build_field(self.spec, label="X", type_key=ft["key"])
            self.assertEqual(se.field_type_of(built), ft["key"], ft["key"])

    # ---- field mutations ---------------------------------------------
    def test_add_field_appends_and_lints_clean(self):
        out = se.add_field(self.spec, "contact", label="Fax number", type_key="phone")
        contact = se.find_section(out, "contact")
        labels = [c["label"] for c in contact["children"]]
        self.assertIn("Fax number", labels)
        self.assertTrue(lint_definition(out).is_clean,
                        [d.message for d in lint_definition(out).errors])

    def test_add_field_unknown_section_is_noop(self):
        out = se.add_field(self.spec, "does-not-exist", label="X", type_key="short_text")
        self.assertEqual(se.all_keys(out), se.all_keys(self.spec))

    def test_update_field_keeps_key(self):
        out = se.update_field(
            self.spec, "contact", "contactName",
            label="Full legal name", type_key="short_text",
        )
        contact = se.find_section(out, "contact")
        fld = next(c for c in contact["children"] if c["key"] == "contactName")
        self.assertEqual(fld["label"], "Full legal name")
        self.assertEqual(fld["key"], "contactName")  # key preserved

    def test_update_field_changes_type(self):
        out = se.update_field(
            self.spec, "contact", "contactName",
            label="Name", type_key="email",
        )
        contact = se.find_section(out, "contact")
        fld = next(c for c in contact["children"] if c["key"] == "contactName")
        self.assertEqual(fld["dataType"], "string")
        self.assertEqual(fld["semanticType"], "email")

    def test_remove_field(self):
        out = se.remove_field(self.spec, "contact", "contactPhone")
        contact = se.find_section(out, "contact")
        self.assertNotIn("contactPhone", [c["key"] for c in contact["children"]])
        self.assertTrue(lint_definition(out).is_clean)

    def test_move_field_up(self):
        contact = se.find_section(self.spec, "contact")
        before = [c["key"] for c in contact["children"]]
        out = se.move_field(self.spec, "contact", before[1], "up")
        after = [c["key"] for c in se.find_section(out, "contact")["children"]]
        self.assertEqual(after[0], before[1])
        self.assertEqual(after[1], before[0])

    def test_move_field_at_edge_is_noop(self):
        contact = se.find_section(self.spec, "contact")
        first = contact["children"][0]["key"]
        out = se.move_field(self.spec, "contact", first, "up")
        self.assertEqual(
            [c["key"] for c in se.find_section(out, "contact")["children"]],
            [c["key"] for c in contact["children"]],
        )

    # ---- section mutations -------------------------------------------
    def test_add_section_numbers_and_lints(self):
        out = se.add_section(self.spec, "Performance Measures")
        secs = se.sections(out)
        self.assertEqual(secs[-1]["label"], "Performance Measures")
        self.assertEqual(secs[-1]["extensions"]["x-section-number"], len(secs))
        self.assertTrue(lint_definition(out).is_clean)

    def test_remove_section_renumbers(self):
        out = se.remove_section(self.spec, "services")
        nums = [s["extensions"]["x-section-number"] for s in se.sections(out)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))
        self.assertNotIn("services", [s["key"] for s in se.sections(out)])

    def test_move_section_down_renumbers(self):
        before = [s["key"] for s in se.sections(self.spec)]
        out = se.move_section(self.spec, before[0], "down")
        after = [s["key"] for s in se.sections(out)]
        self.assertEqual(after[0], before[1])
        nums = [s["extensions"]["x-section-number"] for s in se.sections(out)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))

    def test_update_section_label(self):
        out = se.update_section(self.spec, "budget", "Proposed FY Budget")
        self.assertEqual(se.find_section(out, "budget")["label"], "Proposed FY Budget")

    def test_original_unchanged(self):
        # Mutations must not alias the input.
        n_before = len(se.find_section(self.spec, "contact")["children"])
        se.add_field(self.spec, "contact", label="Z", type_key="short_text")
        n_after = len(se.find_section(self.spec, "contact")["children"])
        self.assertEqual(n_before, n_after)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class DraftLifecycleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.fd = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )

    def test_get_draft_seeds_from_published(self):
        self.fd.draft_schema = None
        draft = se.get_draft_schema(self.fd)
        self.assertEqual(draft.get("name"), "csbg-tribal-plan")
        self.assertFalse(se.has_draft(self.fd))

    def test_save_draft_persists_without_touching_published(self):
        published_before = dict(self.fd.schema)
        draft = se.get_draft_schema(self.fd)
        draft = se.add_field(draft, "contact", label="Mobile", type_key="phone")
        ok, report = se.save_draft(self.fd, draft, user=None)
        self.assertTrue(ok, [d.message for d in report.errors])
        self.fd.refresh_from_db()
        # Published schema unchanged; draft holds the new field.
        self.assertEqual(self.fd.schema, published_before)
        self.assertTrue(se.has_draft(self.fd))
        contact = se.find_section(self.fd.draft_schema, "contact")
        self.assertIn("Mobile", [c["label"] for c in contact["children"]])

    def test_discard_draft_reverts(self):
        draft = se.add_field(se.get_draft_schema(self.fd), "contact", label="X", type_key="short_text")
        se.save_draft(self.fd, draft)
        self.assertTrue(se.has_draft(self.fd))
        se.discard_draft(self.fd)
        self.fd.refresh_from_db()
        self.assertFalse(se.has_draft(self.fd))
        self.assertIsNone(self.fd.draft_schema)
