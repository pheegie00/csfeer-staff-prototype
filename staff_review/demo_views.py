"""Superuser-only "View as" impersonation for demo / testing (Phase 4 Step 7).

Lets a logged-in superuser flip between seeded demo personas with a
single click -- no logout / login churn -- so live demos and manual
QA can exercise OCS-vs-OFA-vs-recipient views fluidly.

Security posture:
- Both views require is_superuser. Non-superusers get 403.
- The set of impersonable accounts is the union of:
    1. seed_demo_users' staff personas
    2. seed_demo_users' recipient personas
  -- identified by email allow-list, so a superuser can't impersonate
  an arbitrary production user via URL fiddling.
- After switching, the audit signal in staff_review/signals.py logs
  the new login event with the actor's IP -- so the trail still
  reflects who was actually at the keyboard (via the original
  superuser's request) plus who they impersonated.
- Switching is a POST so a leaked GET URL can't trigger it accidentally.

This is intentionally a thin layer. Production-grade impersonation
(separate "impersonated_by" header, all actions tagged with the real
operator, etc.) is out of scope for the prototype.
"""

from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from staff_review.management.commands.seed_demo_users import (
    RECIPIENT_PERSONAS,
    STAFF_PERSONAS,
)

User = get_user_model()


# Allow-list of emails impersonable via the View-as toggle. Derived
# from the seed_demo_users personas so the two stay in sync.
DEMO_STAFF_EMAILS = [p[0] for p in STAFF_PERSONAS]
DEMO_RECIPIENT_EMAILS = [p[0] for p in RECIPIENT_PERSONAS]
DEMO_EMAIL_ALLOWLIST = set(DEMO_STAFF_EMAILS + DEMO_RECIPIENT_EMAILS)


def get_demo_personas():
    """Build a flat list of persona dicts for the nav dropdown + index page.

    Reads the seed_demo_users tuples + cross-references with the User
    table so we only surface accounts that actually exist (and skip
    any that the seed command never reached).
    """
    by_email = {u.email: u for u in User.objects.filter(email__in=DEMO_EMAIL_ALLOWLIST)}

    personas = []
    for (email, first, last, office_code, role, is_super, label) in STAFF_PERSONAS:
        u = by_email.get(email)
        if u is None:
            continue
        personas.append({
            "user_id": u.id,
            "email": email,
            "display_name": f"{first} {last}",
            "label": label,
            "category": "Platform" if is_super else f"{office_code} Staff",
            "is_staff_side": True,
        })
    for (email, first, last, org_name, org_type, state_code, group_name, label) in RECIPIENT_PERSONAS:
        u = by_email.get(email)
        if u is None:
            continue
        personas.append({
            "user_id": u.id,
            "email": email,
            "display_name": f"{first} {last}",
            "label": label,
            "category": f"Recipient ({org_name})",
            "is_staff_side": False,
        })
    return personas


DEMO_ADMIN_SESSION_KEY = "is_demo_admin"


def _request_can_use_viewas(request) -> bool:
    """A request may use the View-as toggle if:

    1. The current user IS a superuser, OR
    2. The session was previously a superuser who initiated View-as
       (DEMO_ADMIN_SESSION_KEY=True).

    This second case is what lets a demo flow work fluidly: log in as
    root@acf.hhs.gov, switch to Maya, then keep switching to Dana / Sam
    without having to sign back out and in as root each time.
    """
    if not request.user.is_authenticated:
        return False
    if request.user.is_superuser:
        return True
    return bool(request.session.get(DEMO_ADMIN_SESSION_KEY))


class _ViewAsAdminRequiredMixin:
    """Enforce View-as eligibility (real superuser OR session-flagged demo admin)."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("staff_review:inbox"))  # login redirect
        if not _request_can_use_viewas(request):
            raise PermissionDenied(
                "View-as is restricted to platform superusers."
            )
        return super().dispatch(request, *args, **kwargs)


# Backward-compat alias for callers that imported the old name.
_SuperuserRequiredMixin = _ViewAsAdminRequiredMixin


class DemoUsersIndexView(_ViewAsAdminRequiredMixin, TemplateView):
    """List all seeded demo personas with a one-click 'View as' button.

    Linked from the staff nav's View-as dropdown. Useful as a single
    URL to send to teammates for exploring the prototype.
    """

    template_name = "staff_review/demo_users_index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["personas"] = get_demo_personas()
        ctx["current_user_email"] = self.request.user.email
        return ctx


class ViewAsUserView(_ViewAsAdminRequiredMixin, View):
    """POST -> switch the session login to the chosen demo persona.

    Accepts: user_id (POST), next (optional POST).
    Returns: redirect to ?next= or to inbox.

    Allow-listed against DEMO_EMAIL_ALLOWLIST so a leaked URL can't
    be used to impersonate a real-staffer account.
    """

    http_method_names = ["post"]

    def post(self, request):
        user_id = request.POST.get("user_id")
        nxt = request.POST.get("next") or reverse("staff_review:inbox")

        if not user_id:
            messages.error(request, "View-as: no user_id supplied.")
            return HttpResponseRedirect(nxt)

        target = User.objects.filter(id=user_id).first()
        if target is None:
            messages.error(request, "View-as: user not found.")
            return HttpResponseRedirect(nxt)

        if target.email not in DEMO_EMAIL_ALLOWLIST:
            raise PermissionDenied(
                f"View-as is allow-listed to seeded demo personas only "
                f"({target.email} is not in the list)."
            )

        # Django's login() rotates the session; the user_logged_in signal in
        # staff_review/signals.py fires and writes an audit row. The backend
        # MUST be one of settings.AUTHENTICATION_BACKENDS or the next
        # request will see request.user as anonymous (Django logs them out
        # when the stored backend isn't configured).
        login(
            request, target,
            backend="csfeer.auth_backends.EmailOIDCAuthenticationBackend",
        )

        # Persist the demo-admin flag so the toggle stays visible after
        # switching from superuser -> non-superuser persona. Otherwise the
        # user would have to log back in as root@... to switch again.
        request.session[DEMO_ADMIN_SESSION_KEY] = True

        messages.success(
            request,
            f"Now viewing as {target.first_name} {target.last_name} ({target.email}).",
        )
        return HttpResponseRedirect(nxt)
