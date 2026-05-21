"""Tests for Phase 4 Steps 9 + 10: Help section + Feature flag system.

Help coverage:
- Index renders + lists articles for the logged-in user only
- Audience filtering: a CSBG-only admin sees admin articles + the CSBG-only
  recipient personas DO NOT see admin articles
- Article detail 404s when the slug isn't in the user's audience
- Chatbot returns relevant articles via keyword scoring
- Chatbot's "no match" fallback fires when nothing scores
- Chat history persists in the session across requests

Feature flag coverage:
- Default state: every flag is on; nav items show; URLs reachable
- Toggling a flag off: nav item disappears AND URL returns 503 with friendly page
- Flag admin is superuser-only (NOT just any demo-admin)
- Toggling persists across requests
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from staff_review.feature_flags import (
    REGISTERED_FLAGS,
    FeatureFlag,
    flags_enabled_map,
    is_enabled,
)
from staff_review.help_chatbot import answer as chatbot_answer
from staff_review.help_content import (
    AUD_PLATFORM_ADMIN,
    AUD_PROGRAM_ADMIN,
    AUD_RECIPIENT_AO,
    ARTICLES,
    article_by_slug,
    articles_for,
    audiences_for_user,
)

User = get_user_model()
_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class AudienceDerivationTest(TestCase):
    """audiences_for_user picks the right role tokens per persona."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_superuser_gets_platform_admin(self):
        u = User.objects.get(email="root@acf.hhs.gov")
        self.assertIn(AUD_PLATFORM_ADMIN, audiences_for_user(u))

    def test_csbg_only_admin_gets_program_admin(self):
        u = User.objects.get(email="jordan.lee@acf.hhs.gov")
        auds = audiences_for_user(u)
        self.assertIn(AUD_PROGRAM_ADMIN, auds)
        self.assertNotIn(AUD_PLATFORM_ADMIN, auds)

    def test_reviewer_gets_reviewer(self):
        u = User.objects.get(email="maya.rodriguez@acf.hhs.gov")
        auds = audiences_for_user(u)
        self.assertIn("reviewer", auds)
        self.assertNotIn(AUD_PROGRAM_ADMIN, auds)

    def test_recipient_ao_gets_recipient_ao(self):
        u = User.objects.get(email="tribe-ao@example.com")
        auds = audiences_for_user(u)
        self.assertIn(AUD_RECIPIENT_AO, auds)
        self.assertIn("recipient", auds)
        # Should NOT have staff-side tokens
        self.assertNotIn("reviewer", auds)
        self.assertNotIn(AUD_PROGRAM_ADMIN, auds)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class HelpIndexViewTest(TestCase):
    """Index renders articles filtered to the user's audience."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def _client(self, email):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email=email))
        return c

    def test_index_renders_for_staff(self):
        c = self._client("maya.rodriguez@acf.hhs.gov")
        resp = c.get("/staff/help/")
        self.assertEqual(resp.status_code, 200)
        # Maya is a reviewer; her index should include the reviewer quick start
        self.assertContains(resp, "Getting started as a Federal Reviewer")
        # But NOT the program admin quick start
        self.assertNotContains(resp, "Getting started as a Program Admin")

    def test_index_for_program_admin_shows_form_builder_articles(self):
        c = self._client("dana.chen@acf.hhs.gov")
        resp = c.get("/staff/help/")
        self.assertContains(resp, "How to set a submission window")
        self.assertContains(resp, "How to publish a new version")

    def test_index_for_recipient_shows_recipient_articles_not_staff_articles(self):
        c = self._client("tribe-ao@example.com")
        resp = c.get("/staff/help/")
        self.assertContains(resp, "Getting started as a recipient")
        # Should NOT see staff-only articles
        self.assertNotContains(resp, "How to publish a new version")
        self.assertNotContains(resp, "Understanding the Submissions inbox")

    def test_total_count_matches_filtered_articles(self):
        c = self._client("maya.rodriguez@acf.hhs.gov")
        resp = c.get("/staff/help/")
        expected = len(articles_for(audiences_for_user(
            User.objects.get(email="maya.rodriguez@acf.hhs.gov")
        )))
        self.assertEqual(resp.context["total_articles"], expected)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class HelpArticleViewTest(TestCase):
    """Single article view honours audience filtering."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def _client(self, email):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email=email))
        return c

    def test_article_renders_for_in_audience_user(self):
        c = self._client("dana.chen@acf.hhs.gov")
        resp = c.get("/staff/help/publishing-a-new-version/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Deprecate the current version")

    def test_article_404s_for_out_of_audience_user(self):
        # Tribe AO cannot see the admin-only publish article
        c = self._client("tribe-ao@example.com")
        resp = c.get("/staff/help/publishing-a-new-version/")
        self.assertEqual(resp.status_code, 404)

    def test_unknown_slug_404s(self):
        c = self._client("maya.rodriguez@acf.hhs.gov")
        resp = c.get("/staff/help/no-such-article/")
        self.assertEqual(resp.status_code, 404)

    def test_no_em_dashes_in_any_article_body(self):
        """Style rule: no em dashes in user-facing content."""
        for art in ARTICLES:
            self.assertNotIn("—", art.body,
                f"Article '{art.title}' contains an em dash in body")
            self.assertNotIn("—", art.title,
                f"Article '{art.title}' contains an em dash in title")
            self.assertNotIn("—", art.summary,
                f"Article '{art.title}' contains an em dash in summary")


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class ChatbotTest(TestCase):
    """Keyword scoring matches the right articles for canned questions."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_return_question_finds_return_article(self):
        u = User.objects.get(email="maya.rodriguez@acf.hhs.gov")
        resp = chatbot_answer(u, "how do I return a submission for revision")
        self.assertFalse(resp.fallback)
        titles = {a.title for a in resp.articles}
        self.assertIn("How to return a submission for revision", titles)

    def test_publish_question_finds_publish_article_for_admin(self):
        u = User.objects.get(email="dana.chen@acf.hhs.gov")
        resp = chatbot_answer(u, "how do I publish a new version of a form")
        self.assertFalse(resp.fallback)
        titles = {a.title for a in resp.articles}
        self.assertIn("How to publish a new version", titles)

    def test_synonym_send_back_finds_return_article(self):
        u = User.objects.get(email="maya.rodriguez@acf.hhs.gov")
        resp = chatbot_answer(u, "I need to send this submission back")
        self.assertFalse(resp.fallback)
        slugs = {a.slug for a in resp.articles}
        self.assertIn("returning-a-submission", slugs)

    def test_fallback_when_nothing_matches(self):
        u = User.objects.get(email="maya.rodriguez@acf.hhs.gov")
        resp = chatbot_answer(u, "asdfghjkl qwerty zxcvbn")
        self.assertTrue(resp.fallback)
        self.assertEqual(resp.articles, [])

    def test_audience_filtering_in_chatbot(self):
        # Recipient asks about publishing -- should NOT get the admin article
        u = User.objects.get(email="tribe-ao@example.com")
        resp = chatbot_answer(u, "how do I publish a new version")
        slugs = {a.slug for a in resp.articles}
        self.assertNotIn("publishing-a-new-version", slugs)

    def test_chatbot_view_appends_to_session_history(self):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email="maya.rodriguez@acf.hhs.gov"))
        c.post("/staff/help/chat/", data={"query": "how do I return a submission"})
        history = c.session.get("help_chat_history", [])
        self.assertEqual(len(history), 2)  # user turn + assistant turn
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertGreater(len(history[1]["articles"]), 0)


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FeatureFlagDefaultsTest(TestCase):
    """Every registered flag defaults to enabled."""

    def test_all_flags_default_to_enabled(self):
        m = flags_enabled_map()
        for f in REGISTERED_FLAGS:
            self.assertTrue(m.get(f.key, False),
                f"Flag {f.key} should default to enabled")

    def test_flag_count_matches_registry(self):
        m = flags_enabled_map()
        self.assertEqual(len(m), len(REGISTERED_FLAGS))


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FeatureFlagAdminTest(TestCase):
    """Toggling flags is gated by superuser, takes effect immediately."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def _client(self, email):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email=email))
        return c

    def test_admin_renders_for_superuser(self):
        c = self._client("root@acf.hhs.gov")
        resp = c.get("/staff/features/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Feature flags")

    def test_admin_blocked_for_non_superuser(self):
        c = self._client("dana.chen@acf.hhs.gov")
        resp = c.get("/staff/features/")
        self.assertEqual(resp.status_code, 403)

    def test_toggle_flips_state(self):
        c = self._client("root@acf.hhs.gov")
        self.assertTrue(is_enabled("help_section"))
        c.post("/staff/features/toggle/", data={"key": "help_section"})
        self.assertFalse(is_enabled("help_section"))
        # Toggle again -> back on
        c.post("/staff/features/toggle/", data={"key": "help_section"})
        self.assertTrue(is_enabled("help_section"))

    def test_toggle_blocked_for_non_superuser(self):
        c = self._client("dana.chen@acf.hhs.gov")
        resp = c.post("/staff/features/toggle/", data={"key": "help_section"})
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(is_enabled("help_section"))


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class FeatureFlagGatingTest(TestCase):
    """Flag-off shows the disabled page; flag-on lets the URL through."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        # Materialize all flag rows so .update() calls in tests target real rows.
        flags_enabled_map()

    def _client(self, email):
        c = Client(HTTP_HOST="localhost")
        c.force_login(User.objects.get(email=email))
        return c

    def test_help_url_blocked_when_flag_off(self):
        FeatureFlag.objects.filter(key="help_section").update(is_enabled=False)
        c = self._client("maya.rodriguez@acf.hhs.gov")
        resp = c.get("/staff/help/")
        self.assertEqual(resp.status_code, 503)
        self.assertContains(resp, "currently off", status_code=503)

    def test_form_builder_url_blocked_when_flag_off(self):
        FeatureFlag.objects.filter(key="form_builder").update(is_enabled=False)
        c = self._client("dana.chen@acf.hhs.gov")
        resp = c.get("/staff/form-builder/")
        self.assertEqual(resp.status_code, 503)

    def test_exports_url_blocked_when_flag_off(self):
        FeatureFlag.objects.filter(key="csv_exports").update(is_enabled=False)
        c = self._client("riley.brooks@acf.hhs.gov")
        resp = c.get("/staff/exports/")
        self.assertEqual(resp.status_code, 503)

    def test_audit_log_url_blocked_when_flag_off(self):
        FeatureFlag.objects.filter(key="audit_log_viewer").update(is_enabled=False)
        c = self._client("root@acf.hhs.gov")
        resp = c.get("/staff/audit-log/")
        self.assertEqual(resp.status_code, 503)

    def test_nav_hides_help_when_flag_off(self):
        FeatureFlag.objects.filter(key="help_section").update(is_enabled=False)
        c = self._client("maya.rodriguez@acf.hhs.gov")
        resp = c.get("/staff/")
        # Help nav link should not appear
        self.assertNotContains(resp, ">Help</a>")

    def test_view_as_blocked_when_flag_off(self):
        FeatureFlag.objects.filter(key="view_as_toggle").update(is_enabled=False)
        c = self._client("root@acf.hhs.gov")
        # Even superuser cannot use view-as when the flag is off
        resp = c.get("/staff/demo-users/")
        self.assertEqual(resp.status_code, 403)
