"""Permission scoping tests for staff_review (CORE-132, CORE-29, CORE-192).

Verifies:
- StaffRequiredMixin blocks non-Federal-Staff users (403)
- Unauthenticated users get redirected to login
- Federal Staff group membership grants access to every staff_review URL
- Superusers always pass
- staff_queryset_filter returns empty for non-staff, full queryset for staff

Run:
    uv run python manage.py test staff_review.test_permissions
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from form_manager.models.forms import FormEntry
from staff_review.permissions import FEDERAL_STAFF_GROUP, staff_queryset_filter

User = get_user_model()

_TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "oauth2_authcodeflow" not in m]

# Every URL the mixin protects (mirrors staff_review/urls.py)
PROTECTED_URLS = [
    "/staff/",
    "/staff/sub/s1/",
    "/staff/sub/s1/edit/",
    "/staff/sub/s1/return/",
    "/staff/sub/s1/determination/",
    "/staff/exports/",
    "/staff/audit-log/",
    "/staff/form-builder/",
]


@override_settings(MIDDLEWARE=_TEST_MIDDLEWARE)
class StaffPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)
        cls.staff_user = User.objects.get(email="m.rodriguez@acf.hhs.gov")
        cls.recipient_user = User.objects.get(email="recipient-viewer@example.com")

    def _client(self, user=None):
        c = Client(HTTP_HOST="localhost")
        if user is not None:
            c.force_login(user)
        return c

    # ----- CORE-132 -----

    def test_federal_staff_group_exists_with_permissions(self):
        g = Group.objects.get(name=FEDERAL_STAFF_GROUP)
        codenames = set(g.permissions.values_list("codename", flat=True))
        self.assertEqual(codenames, {
            "staff_view_any_submission",
            "staff_edit_on_behalf",
            "staff_return_submission",
            "staff_determine_submission",
            "staff_archive_submission",
        })

    def test_demo_staff_user_is_in_federal_staff_group(self):
        self.assertTrue(
            self.staff_user.groups.filter(name=FEDERAL_STAFF_GROUP).exists(),
            "seed_demo_data should add Maya Rodriguez to Federal Staff group",
        )

    def test_recipient_user_is_NOT_in_federal_staff_group(self):
        self.assertFalse(
            self.recipient_user.groups.filter(name=FEDERAL_STAFF_GROUP).exists(),
        )

    # ----- Per-URL access checks -----

    def test_staff_user_can_access_all_protected_urls(self):
        c = self._client(self.staff_user)
        for url in PROTECTED_URLS:
            resp = c.get(url)
            self.assertIn(resp.status_code, (200, 302),
                          f"Federal Staff should reach {url} (got {resp.status_code})")

    def test_recipient_user_blocked_from_all_protected_urls(self):
        c = self._client(self.recipient_user)
        for url in PROTECTED_URLS:
            resp = c.get(url)
            self.assertEqual(resp.status_code, 403,
                             f"Non-staff user should get 403 on {url} (got {resp.status_code})")

    def test_unauthenticated_user_redirected_to_login(self):
        c = self._client(None)  # no force_login
        resp = c.get("/staff/")
        self.assertEqual(resp.status_code, 302)
        # LoginRequiredMixin redirects to settings.LOGIN_URL
        self.assertIn("login", resp.url.lower())

    # ----- CORE-29 -----

    def test_staff_queryset_filter_returns_everything_for_staff(self):
        all_entries = FormEntry.objects.all()
        filtered = staff_queryset_filter(all_entries, self.staff_user)
        self.assertEqual(filtered.count(), all_entries.count())

    def test_staff_queryset_filter_returns_empty_for_recipient(self):
        filtered = staff_queryset_filter(FormEntry.objects.all(), self.recipient_user)
        self.assertEqual(filtered.count(), 0)

    def test_staff_queryset_filter_returns_empty_for_anonymous(self):
        from django.contrib.auth.models import AnonymousUser
        filtered = staff_queryset_filter(FormEntry.objects.all(), AnonymousUser())
        self.assertEqual(filtered.count(), 0)

    # ----- Superuser override -----

    def test_superuser_bypasses_group_check(self):
        super_u = User.objects.create_superuser(
            email="super@example.com", password="x"
        )
        c = self._client(super_u)
        resp = c.get("/staff/")
        self.assertEqual(resp.status_code, 200)

    # ----- POST verbs are also protected -----

    def test_recipient_cannot_POST_to_protected_actions(self):
        from staff_review.models import FormReturn
        baseline = FormReturn.objects.count()  # seed already creates some (Navajo, Kawerak)

        c = self._client(self.recipient_user)
        # Try to fire a return -- must 403
        resp = c.post("/staff/sub/s1/return/send/", data={"item-1-text": "x"})
        self.assertEqual(resp.status_code, 403)

        # No new FormReturn created by the blocked POST
        self.assertEqual(FormReturn.objects.count(), baseline)
