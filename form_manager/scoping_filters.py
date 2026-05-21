"""Recipient-side enforcement of FormScoping + SubmissionWindow (Batch H).

The staff-side Form Builder lets program admins define WHO can fill out
a form (`FormScoping.scope_to_org_types`) and WHEN (`SubmissionWindow`).
This module enforces those rules on the recipient experience:

  - `forms_available_to_org()` filters the "Available Forms" list down to
    templates the org is actually in scope for.
  - `window_state_for()` derives a (status, message, can_start) triple for
    a given (form_definition, fiscal_year) so the recipient UI can render
    badges + disable / hide the Start button.
  - `assert_can_start_form()` raises PermissionDenied if a recipient tries
    to bypass the UI and POST directly to /forms/start/<id>/.

Rules (Phase II + Batch H):

  Scope:
    - If FormScoping doesn't exist for a form -> no enforcement (legacy
      behavior; backward compat with pre-CORE-22 forms).
    - Otherwise, the org is in-scope iff org.org_type is in
      scope_to_org_types OR the org is in explicit_orgs.

  Window (per CORE-25):
    - If no SubmissionWindow exists for the current FY -> always available
      (ad-hoc forms like CSBG Eligible Entity List).
    - status="upcoming"   -> badge "Opens MM/DD/YY", Start button hidden.
    - status="open"       -> badge "Closes in N days" (only if <30 days),
                             Start button enabled.
    - status="past_due"   -> badge "Closed MM/DD/YY", Start hidden.
                             Per CORE-25, existing drafts remain editable.
"""

from dataclasses import dataclass
from typing import Iterable, Optional

from django.utils import timezone

# Default fiscal year used when no current_fy is supplied. Matches the
# staff-side Form Builder default in form_builder_views.py.
DEFAULT_CURRENT_FY = "FY26"


@dataclass(frozen=True)
class WindowState:
    """Derived state of a SubmissionWindow for the recipient UI."""

    status: str        # "open" | "upcoming" | "past_due" | "always_open"
    can_start: bool    # may a recipient start a new draft right now?
    badge_label: str   # short label for a UI badge (may be "")
    badge_tone: str    # USWDS-ish tone: "info" | "warn" | "error" | ""
    detail: str        # longer message for tooltips / inline help


_BADGE_TONE_BY_STATUS = {
    "upcoming": "info",
    "open": "info",
    "past_due": "error",
    "always_open": "",
}


def window_state_for(form_def, current_fy: str = DEFAULT_CURRENT_FY) -> WindowState:
    """Compute the recipient-facing window state for a form."""
    window = form_def.submission_windows.filter(fiscal_year=current_fy).first()
    if window is None:
        return WindowState(
            status="always_open", can_start=True, badge_label="",
            badge_tone="", detail="No submission window defined; ad-hoc submissions accepted.",
        )

    status = window.status
    if status == "upcoming":
        opens = window.opens_at
        return WindowState(
            status=status, can_start=False,
            badge_label=f"Opens {opens:%b %-d, %Y}",
            badge_tone="info",
            detail=(
                f"This form opens for {current_fy} on {opens:%B %-d, %Y}. "
                f"You can start a new draft once the window opens."
            ),
        )
    if status == "past_due":
        closed = window.closes_at
        return WindowState(
            status=status, can_start=False,
            badge_label=f"Closed {closed:%b %-d, %Y}",
            badge_tone="error",
            detail=(
                f"The {current_fy} submission window closed on {closed:%B %-d, %Y}. "
                f"New drafts cannot be started; existing drafts remain editable."
            ),
        )
    # status == "open"
    days_until_close = window.days_until_close
    if 0 <= days_until_close <= 30:
        badge = f"Closes in {days_until_close} day{'s' if days_until_close != 1 else ''}"
        tone = "warn" if days_until_close <= 7 else "info"
    else:
        badge = "Open"
        tone = "info"
    return WindowState(
        status=status, can_start=True, badge_label=badge, badge_tone=tone,
        detail=f"This form is open for {current_fy} submissions through "
               f"{window.closes_at:%B %-d, %Y}.",
    )


def org_is_in_scope(form_def, org) -> bool:
    """True if org is allowed to fill out form_def per its FormScoping.

    Forms without scoping configured fall back to permissive (legacy
    behavior pre-CORE-22).
    """
    if org is None:
        return False
    scoping = getattr(form_def, "scoping", None)
    if scoping is None:
        return True  # No scoping = no restriction
    # No rules at all = no one is in scope (defensive: scope must be set
    # to allow anyone). But empty lists are the migration default --
    # treat empty as permissive for backward compat with pre-CORE-22 forms.
    if not scoping.scope_to_org_types and not scoping.explicit_orgs.exists():
        return True
    return scoping.is_org_in_scope(org)


def forms_available_to_org(
    queryset,
    org,
    current_fy: str = DEFAULT_CURRENT_FY,
):
    """Filter a FormDefinition queryset to those an org should see.

    Visibility rule: in-scope OR no scoping configured. Window status is
    NOT used to filter -- upcoming / past-due forms still appear in the
    list with a badge explaining why Start is disabled. That preserves
    discoverability ("CSBG Plan opens July 1").
    """
    if org is None:
        return queryset.none()

    # Cheap pre-filter on org_type (Postgres can use it as a JSONField
    # contains query). Then do the precise check in Python for any forms
    # with explicit_orgs membership.
    eligible_ids = []
    for fd in queryset.select_related("scoping").prefetch_related("scoping__explicit_orgs"):
        if org_is_in_scope(fd, org):
            eligible_ids.append(fd.pk)
    return queryset.filter(pk__in=eligible_ids)


def annotate_window_state(form_defs: Iterable, current_fy: str = DEFAULT_CURRENT_FY):
    """Attach a `.window_state` attribute to each FormDefinition for templates."""
    for fd in form_defs:
        fd.window_state = window_state_for(fd, current_fy=current_fy)
    return form_defs


# ----------------------------------------------------------------------
# Hard-stop enforcement for the form_start view
# ----------------------------------------------------------------------

class FormStartBlocked(Exception):
    """Raised when a recipient can't start a new draft of form_def for org."""

    def __init__(self, reason_code: str, message: str):
        self.reason_code = reason_code
        self.message = message
        super().__init__(message)


def assert_can_start_form(form_def, org, current_fy: str = DEFAULT_CURRENT_FY) -> None:
    """Raise FormStartBlocked if recipient cannot start a new draft.

    Three failure modes:
      out_of_scope    -- org_type not in scope_to_org_types + not explicit.
      window_upcoming -- current FY's window hasn't opened yet.
      window_past_due -- current FY's window has closed.

    Callers (form_start view) should catch + redirect with messages.error.
    """
    if not org_is_in_scope(form_def, org):
        scoping = getattr(form_def, "scoping", None)
        types = scoping.scope_to_org_types if scoping else []
        raise FormStartBlocked(
            "out_of_scope",
            f"This form is scoped to: {', '.join(types) or '(no orgs)'}. "
            f"Your organization ({org.get_org_type_display()}) is not in scope.",
        )

    state = window_state_for(form_def, current_fy=current_fy)
    if not state.can_start:
        raise FormStartBlocked(
            f"window_{state.status}",
            state.detail,
        )
