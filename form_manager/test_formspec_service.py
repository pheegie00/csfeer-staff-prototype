"""Tests for STAFF-MP-13: Formspec runtime integration.

Covers the service wrapper around formspec-py:
- lint_definition() returns clean for our packaged Tribal Plan spec
- lint_definition() reports errors when given a broken spec
- validate_response() runs without exception against a partial payload
- load_builtin_spec() loads the packaged Tribal Plan
- changelog_between() returns a suggested bump
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from form_manager.models import FormDefinition
from form_manager.services.formspec_service import (
    FORMSPEC_AVAILABLE,
    changelog_between,
    lint_definition,
    load_builtin_spec,
    validate_response,
)

User = get_user_model()
_TEST_MIDDLEWARE = [
    m for m in settings.MIDDLEWARE
    if "oauth2_authcodeflow" not in m and "LoginRequiredMiddlewareWithCurrentPath" not in m
]


class FormspecServiceTest(TestCase):
    """Unit tests for the formspec service wrapper."""

    def test_formspec_lib_is_available(self):
        # Sanity check -- the lib should be installed via uv add.
        self.assertTrue(FORMSPEC_AVAILABLE,
            "formspec-py should be installed; check pyproject.toml.")

    def test_load_builtin_tribal_plan_returns_a_dict(self):
        spec = load_builtin_spec("csbg_tribal_plan")
        self.assertIsNotNone(spec, "Tribal Plan formspec doc should exist.")
        self.assertEqual(spec["$formspec"], "1.0")
        self.assertEqual(spec["name"], "csbg-tribal-plan")
        self.assertIn("items", spec)
        self.assertEqual(len(spec["items"]), 8, "Should have 8 sections.")

    def test_load_builtin_returns_none_for_unknown(self):
        self.assertIsNone(load_builtin_spec("nonexistent"))

    def test_tribal_plan_spec_lints_clean(self):
        spec = load_builtin_spec("csbg_tribal_plan")
        report = lint_definition(spec)
        self.assertTrue(
            report.is_clean,
            f"Tribal Plan spec should lint clean. Errors: {[d.message for d in report.errors]}",
        )

    def test_lint_reports_errors_on_broken_spec(self):
        broken = {"$formspec": "1.0", "items": [{"type": "field"}]}  # missing key + dataType
        report = lint_definition(broken)
        self.assertGreater(report.error_count, 0,
            "Broken spec should produce at least one lint error.")

    def test_lint_handles_empty_input_gracefully(self):
        report = lint_definition({})
        self.assertFalse(report.is_clean)
        self.assertTrue(any(d.code == "X001" for d in report.diagnostics))

    def test_validate_response_returns_result_object(self):
        spec = load_builtin_spec("csbg_tribal_plan")
        sample = {
            "org": {"name": "Cherokee Nation", "uei": "QXYZ12AB34CD"},
            "contact": {"contactName": "Sarah", "contactEmail": "s@example.org"},
        }
        result = validate_response(spec, sample)
        # We don't require valid=True here -- the spec has many required-ish
        # fields without explicit `required` markers, so partial data may not
        # be 'valid'. What matters is the wrapper runs without exception and
        # returns the structured result.
        self.assertIsNotNone(result)
        self.assertIsInstance(result.data, dict)

    def test_validate_response_no_spec_returns_valid(self):
        # When form_def.schema is empty (legacy forms), validation should
        # not block -- return valid so saves go through.
        result = validate_response({}, {"anything": "goes"})
        self.assertTrue(result.valid)

    def test_changelog_between_returns_bump_suggestion(self):
        a = load_builtin_spec("csbg_tribal_plan")
        b = dict(a)
        b["version"] = "1.0.1"
        cl = changelog_between(a, b)
        self.assertIn("suggested_bump", cl)
        # The bump should be one of the standard semver tokens.
        self.assertIn(cl["suggested_bump"], ("major", "minor", "patch"))


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormBuilderFormspecIntegrationTest(TestCase):
    """Form Builder Detail surfaces the Formspec lint + spec viewer."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="dana.chen@acf.hhs.gov")
        cls.tribal_plan = FormDefinition.objects.get(
            name="CSBG Model Tribal Plan", variant="1.0.0",
        )

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        return c

    def test_seed_populates_tribal_plan_schema_with_formspec_doc(self):
        # Seed should have replaced the {} schema with the real spec.
        self.assertEqual(self.tribal_plan.schema.get("$formspec"), "1.0")
        self.assertEqual(self.tribal_plan.schema.get("name"), "csbg-tribal-plan")

    def test_form_builder_detail_shows_runtime_card_when_flag_on(self):
        c = self._client()
        resp = c.get(f"/staff/form-builder/{self.tribal_plan.id}/")
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        self.assertIn("Form runtime", body)
        self.assertIn("View spec", body)
        self.assertIn("Clean", body, "Tribal Plan should show 'Clean' lint badge.")
        # And the pretty-printed JSON should be in the page (inside the dialog).
        self.assertIn("$formspec", body)

    def test_form_builder_detail_hides_runtime_card_when_flag_off(self):
        from staff_review.feature_flags import FeatureFlag, flags_enabled_map
        flags_enabled_map()  # materialize rows
        FeatureFlag.objects.filter(key="form_runtime").update(is_enabled=False)
        c = self._client()
        resp = c.get(f"/staff/form-builder/{self.tribal_plan.id}/")
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        self.assertNotIn("Form runtime", body)
        self.assertNotIn("View spec", body)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormspecPreviewViewTest(TestCase):
    """The /forms/entry/<id>/render/ recipient-side route."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="dana.chen@acf.hhs.gov")
        # Find a seeded Tribal Plan FormEntry to preview
        from form_manager.models import FormEntry
        cls.entry = FormEntry.objects.filter(
            form_definition__name="CSBG Model Tribal Plan",
        ).first()
        cls.assertions_ready = cls.entry is not None

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff_user)
        return c

    def test_preview_returns_html_when_spec_present_and_flag_on(self):
        self.assertTrue(self.assertions_ready, "Need a seeded Tribal Plan FormEntry.")
        c = self._client()
        resp = c.get(f"/forms/entry/{self.entry.id}/render/")
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        # Should embed the spec + the web component script
        self.assertIn("formspec-render", body)
        self.assertIn("$formspec", body)
        self.assertIn("@formspec-org/webcomponent", body)

    def test_preview_404s_when_flag_off(self):
        from staff_review.feature_flags import FeatureFlag, flags_enabled_map
        flags_enabled_map()
        FeatureFlag.objects.filter(key="form_runtime").update(is_enabled=False)
        c = self._client()
        resp = c.get(f"/forms/entry/{self.entry.id}/render/")
        self.assertEqual(resp.status_code, 404)

    def test_preview_404s_when_form_has_no_spec(self):
        # Find a FormDefinition with no real spec
        from form_manager.models import FormDefinition, FormEntry
        no_spec_def = FormDefinition.objects.exclude(
            name="CSBG Model Tribal Plan",
        ).filter(is_active=True).first()
        self.assertIsNotNone(no_spec_def)
        # Make sure its schema is empty
        self.assertNotEqual(no_spec_def.schema.get("$formspec"), "1.0",
            f"Expected no spec on {no_spec_def.name}.")
        # Need an entry on that form to GET preview
        entry = FormEntry.objects.filter(form_definition=no_spec_def).first()
        if entry is None:
            entry = FormEntry.objects.create(
                form_definition=no_spec_def,
                organization=self.entry.organization,
                created_by=self.staff_user,
                data={}, status="submitted",
            )
        c = self._client()
        resp = c.get(f"/forms/entry/{entry.id}/render/")
        self.assertEqual(resp.status_code, 404)

    def test_preview_post_saves_data_and_returns_json(self):
        import json
        c = self._client()
        url = f"/forms/entry/{self.entry.id}/render/"
        payload = {
            "data": {
                "org": {"name": "Test Tribe Updated", "uei": "TST1234ABCD"},
                "contact": {"contactName": "Updated", "contactEmail": "u@example.gov"},
            },
        }
        resp = c.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.content.decode())
        self.assertTrue(body["ok"])
        self.assertIn("valid", body)
        self.assertIn("item_count", body)
        # And data should be persisted
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.data["org"]["name"], "Test Tribe Updated")
