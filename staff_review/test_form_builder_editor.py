"""Tests for the visual Form Builder editor views + draft/publish wiring (STAFF-MP-14)."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from form_manager.models import FormDefinition, FormEntry
from form_manager.services import schema_editor as se
from staff_review.publish_service import publish_new_version

User = get_user_model()
_TEST_MIDDLEWARE = [
    m for m in settings.MIDDLEWARE
    if "oauth2_authcodeflow" not in m and "LoginRequiredMiddlewareWithCurrentPath" not in m
]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FormBuilderEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff = User.objects.get(email="dana.chen@acf.hhs.gov")
        cls.fd = FormDefinition.objects.get(name="CSBG Model Tribal Plan", variant="1.0.0")

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff)
        return c

    def _url(self):
        return f"/staff/form-builder/{self.fd.id}/edit/"

    def test_get_renders_editor_with_sections(self):
        resp = self._client().get(self._url())
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        self.assertIn("Edit fields", body)
        self.assertIn("Primary Contact", body)        # a section label
        self.assertIn("Add field to this section", body)
        self.assertIn("Add a new section", body)

    def test_add_field_creates_draft_without_touching_published(self):
        published_before = dict(self.fd.schema)
        resp = self._client().post(self._url(), {
            "action": "add_field",
            "section_key": "contact",
            "label": "Mobile phone",
            "field_type": "phone",
            "help": "Cell is fine",
        })
        self.assertEqual(resp.status_code, 302)
        self.fd.refresh_from_db()
        self.assertEqual(self.fd.schema, published_before)   # published untouched
        self.assertTrue(se.has_draft(self.fd))
        contact = se.find_section(self.fd.draft_schema, "contact")
        self.assertIn("Mobile phone", [c["label"] for c in contact["children"]])

    def test_remove_field_on_draft(self):
        c = self._client()
        c.post(self._url(), {"action": "remove_field", "section_key": "contact", "field_key": "contactPhone"})
        self.fd.refresh_from_db()
        contact = se.find_section(self.fd.draft_schema, "contact")
        self.assertNotIn("contactPhone", [ch["key"] for ch in contact["children"]])

    def test_add_section_then_field(self):
        c = self._client()
        c.post(self._url(), {"action": "add_section", "label": "Performance Measures"})
        self.fd.refresh_from_db()
        keys = [s["key"] for s in se.sections(self.fd.draft_schema)]
        new_key = keys[-1]
        self.assertEqual(se.find_section(self.fd.draft_schema, new_key)["label"], "Performance Measures")

    def test_discard_draft_reverts(self):
        c = self._client()
        c.post(self._url(), {"action": "add_field", "section_key": "contact", "label": "X", "field_type": "short_text"})
        self.fd.refresh_from_db()
        self.assertTrue(se.has_draft(self.fd))
        c.post(self._url(), {"action": "discard_draft"})
        self.fd.refresh_from_db()
        self.assertFalse(se.has_draft(self.fd))

    def test_detail_shows_edit_button_and_draft_badge(self):
        c = self._client()
        # No draft yet -> Edit fields present, no draft badge
        body = c.get(f"/staff/form-builder/{self.fd.id}/").content.decode()
        self.assertIn("Edit fields", body)
        # Create a draft -> badge appears
        c.post(self._url(), {"action": "add_field", "section_key": "contact", "label": "X", "field_type": "short_text"})
        body2 = c.get(f"/staff/form-builder/{self.fd.id}/").content.decode()
        self.assertIn("Draft", body2)

    def test_editor_404s_on_non_schema_form(self):
        # A legacy (non-formspec) form in the SAME program the staff user
        # manages -- so we exercise the schema check (404), not the
        # permission check (403). We clone the Tribal Plan's program/family
        # and give it an empty schema.
        legacy = FormDefinition.objects.create(
            name=self.fd.name,
            variant="0.9.0",
            family=self.fd.family,
            schema={},                      # no $formspec -> not editable
            schema_class=self.fd.schema_class,
            program=self.fd.program,
            cycle_type=self.fd.cycle_type,
            is_active=True,
        )
        resp = self._client().get(f"/staff/form-builder/{legacy.id}/edit/")
        self.assertEqual(resp.status_code, 404)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class DraftPreviewViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff = User.objects.get(email="dana.chen@acf.hhs.gov")
        cls.fd = FormDefinition.objects.get(name="CSBG Model Tribal Plan", variant="1.0.0")

    def _client(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(self.staff)
        return c

    def test_draft_preview_renders_draft_schema(self):
        # Stage a draft with a distinctive new field label.
        draft = se.add_field(se.get_draft_schema(self.fd), "contact",
                             label="Distinctive Draft Field", type_key="short_text")
        se.save_draft(self.fd, draft)
        resp = self._client().get(f"/forms/draft-preview/{self.fd.id}/")
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        self.assertIn("Draft preview", body)
        self.assertIn("Distinctive Draft Field", body)
        # Read-only: no Save draft button.
        self.assertNotIn('id="save-btn"', body)

    def test_draft_preview_falls_back_to_published_when_no_draft(self):
        resp = self._client().get(f"/forms/draft-preview/{self.fd.id}/")
        self.assertEqual(resp.status_code, 200)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class PublishConsumesDraftTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff = User.objects.get(email="dana.chen@acf.hhs.gov")
        cls.fd = FormDefinition.objects.get(name="CSBG Model Tribal Plan", variant="1.0.0")

    def test_publish_carries_draft_into_new_version_and_clears_it(self):
        # Stage a draft.
        draft = se.add_field(se.get_draft_schema(self.fd), "contact",
                             label="Carried Field", type_key="short_text")
        se.save_draft(self.fd, draft)
        self.assertTrue(se.has_draft(self.fd))

        new_fd, affected = publish_new_version(
            source_form_def=self.fd, new_variant="1.1.0", actor=self.staff,
            clone_scoping=False, clone_current_window=False,
        )

        # New version's published schema contains the drafted field...
        contact = se.find_section(new_fd.schema, "contact")
        self.assertIn("Carried Field", [c["label"] for c in contact["children"]])
        # ...the spec version was bumped...
        self.assertEqual(new_fd.schema.get("version"), "1.1.0")
        # ...and the source draft is cleared + deprecated.
        self.fd.refresh_from_db()
        self.assertIsNone(self.fd.draft_schema)
        self.assertFalse(self.fd.is_active)

    def test_publish_without_draft_clones_published(self):
        new_fd, _ = publish_new_version(
            source_form_def=self.fd, new_variant="2.0.0", actor=self.staff,
            clone_scoping=False, clone_current_window=False,
        )
        # Same field set as the published source.
        self.assertEqual(
            [s["key"] for s in se.sections(new_fd.schema)],
            [s["key"] for s in se.sections(self.fd.schema)],
        )
