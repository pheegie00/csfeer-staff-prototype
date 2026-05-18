"""Service-layer helpers for submission window lookup and enforcement.

The federal fiscal year is a fixed accounting concept (Oct 1 - Sep 30); there
is no FiscalYear model. The integer FY is the ending calendar year (FY25 =
2025, covering Oct 1 2024 - Sep 30 2025). Keep all FY math here so views and
models stay simple.
"""

from __future__ import annotations

from datetime import date

from django.utils import timezone

from form_manager.models import FormDefinition, FormEntry, SubmissionWindow


def current_fiscal_year(today: date | None = None) -> int:
    """Return the federal FY (ending calendar year) for ``today``.

    October-December roll into the next FY (FY ends Sept 30).
    """
    today = today or timezone.localdate()
    return today.year + 1 if today.month >= 10 else today.year


def fy_label(fiscal_year: int) -> str:
    """``2025 -> "FY25"``."""
    return f"FY{fiscal_year % 100:02d}"


def fy_bounds(fiscal_year: int) -> tuple[date, date]:
    """Return ``(starts_on, ends_on)`` for the given FY."""
    return date(fiscal_year - 1, 10, 1), date(fiscal_year, 9, 30)


def get_active_window(form_definition: FormDefinition) -> SubmissionWindow | None:
    """Return the "current or next" window for ``form_definition``.

    That's the window whose ``closes_at >= today`` with the earliest
    ``opens_at``. Returns ``None`` if no such window exists (i.e. every
    configured window has already closed, or none are configured).
    """
    today = timezone.localdate()
    return (
        SubmissionWindow.objects.filter(form_definition=form_definition, closes_at__gte=today)
        .order_by("opens_at")
        .first()
    )


def can_create_draft(
    form_definition: FormDefinition,
) -> tuple[bool, str, SubmissionWindow | None]:
    """Whether a new draft may be started for ``form_definition`` right now.

    Allowed when an active or upcoming window exists. Returns
    ``(allowed, reason, window)``: ``reason`` is empty on success and a
    human-readable explanation otherwise.
    """
    window = get_active_window(form_definition)
    if window is None:
        return (
            False,
            f"No open submission window for {form_definition.name}.",
            None,
        )
    return True, "", window


def can_submit_draft(form_entry: FormEntry) -> tuple[bool, str]:
    """Whether ``form_entry`` may be submitted right now.

    Allowed when the entry's window is currently open or already past due.
    Legacy entries with no stamped ``fiscal_year`` are allowed through so
    existing user drafts are not retroactively locked out.
    """
    if form_entry.status == FormEntry.STATUS_CLOSED_WITHOUT_ACCEPTANCE:
        return False, "This draft was closed because the fiscal year rolled over."

    if form_entry.fiscal_year is None:
        return True, ""

    window = SubmissionWindow.objects.filter(
        form_definition=form_entry.form_definition,
        fiscal_year=form_entry.fiscal_year,
    ).first()
    if window is None:
        return (
            False,
            f"No submission window configured for {form_entry.form_definition.name} "
            f"{fy_label(form_entry.fiscal_year)}.",
        )

    if window.status == SubmissionWindow.STATUS_UPCOMING:
        return False, f"Submission window opens on {window.opens_at:%B %-d, %Y}."
    return True, ""


def close_stale_drafts(window: SubmissionWindow) -> int:
    """Close prior-FY drafts for the same form as ``window``.

    Sets ``status = closed_without_acceptance`` on every ``FormEntry`` for the
    same ``form_definition`` whose ``fiscal_year`` is earlier than the given
    window's and whose status is still ``draft``. Submitted, amended, and
    already-closed entries are left alone. Returns the number of rows updated.
    """
    return FormEntry.objects.filter(
        form_definition=window.form_definition,
        fiscal_year__lt=window.fiscal_year,
        fiscal_year__isnull=False,
        status=FormEntry.STATUS_DRAFT,
    ).update(status=FormEntry.STATUS_CLOSED_WITHOUT_ACCEPTANCE)
