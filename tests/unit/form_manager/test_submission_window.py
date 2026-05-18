from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from form_manager.models import FormDefinition, FormEntry, SubmissionWindow
from form_manager.submission_windows import (
    can_create_draft,
    can_submit_draft,
    close_stale_drafts,
    current_fiscal_year,
    fy_bounds,
    fy_label,
    get_active_window,
)


# ─── FY math ─────────────────────────────────────────────────────────────────


def test_current_fiscal_year_in_summer():
    """Apr-Sep are within the FY that ends Sep 30 of the same calendar year."""
    assert current_fiscal_year(date(2025, 6, 15)) == 2025


def test_current_fiscal_year_in_fall_rolls_over():
    """Oct-Dec are in the next FY (FY ends Sep 30)."""
    assert current_fiscal_year(date(2025, 10, 1)) == 2026
    assert current_fiscal_year(date(2025, 12, 31)) == 2026


def test_current_fiscal_year_fy_start_boundary():
    """Sep 30 is the last day of FY25; Oct 1 is the first day of FY26."""
    assert current_fiscal_year(date(2025, 9, 30)) == 2025
    assert current_fiscal_year(date(2025, 10, 1)) == 2026


def test_fy_label_format():
    assert fy_label(2025) == "FY25"
    assert fy_label(2030) == "FY30"


def test_fy_bounds():
    assert fy_bounds(2025) == (date(2024, 10, 1), date(2025, 9, 30))


# ─── Model ───────────────────────────────────────────────────────────────────


@pytest.mark.django_db
def test_save_fills_dates_from_fiscal_year_when_blank(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None

    window = SubmissionWindow.objects.create(form_definition=form_def, fiscal_year=2027)

    assert window.opens_at == date(2026, 10, 1)
    assert window.closes_at == date(2027, 9, 30)


@pytest.mark.django_db
def test_save_preserves_explicit_dates(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None

    window = SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=2027,
        opens_at=date(2026, 7, 1),
        closes_at=date(2026, 9, 1),
    )

    assert window.opens_at == date(2026, 7, 1)
    assert window.closes_at == date(2026, 9, 1)


@pytest.mark.django_db
def test_clean_rejects_closes_at_before_opens_at(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    window = SubmissionWindow(
        form_definition=form_def,
        fiscal_year=2027,
        opens_at=date(2026, 9, 1),
        closes_at=date(2026, 7, 1),
    )

    with pytest.raises(ValidationError):
        window.clean()


def test_status_on_returns_upcoming_open_past_due():
    window = SubmissionWindow(
        fiscal_year=2025, opens_at=date(2025, 6, 1), closes_at=date(2025, 8, 1)
    )

    assert window.status_on(date(2025, 5, 31)) == SubmissionWindow.STATUS_UPCOMING
    assert window.status_on(date(2025, 6, 1)) == SubmissionWindow.STATUS_OPEN
    assert window.status_on(date(2025, 7, 15)) == SubmissionWindow.STATUS_OPEN
    assert window.status_on(date(2025, 8, 1)) == SubmissionWindow.STATUS_OPEN
    assert window.status_on(date(2025, 8, 2)) == SubmissionWindow.STATUS_PAST_DUE


# ─── get_active_window ───────────────────────────────────────────────────────


@pytest.mark.django_db
def test_get_active_window_prefers_open_over_upcoming(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    today = date.today()

    # Replace the seed_data window with a known set.
    SubmissionWindow.objects.filter(form_definition=form_def).delete()

    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year,
        opens_at=today - timedelta(days=30),
        closes_at=today + timedelta(days=30),
    )
    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year + 1,
        opens_at=today + timedelta(days=60),
        closes_at=today + timedelta(days=120),
    )

    window = get_active_window(form_def)
    assert window is not None
    assert window.fiscal_year == today.year


@pytest.mark.django_db
def test_get_active_window_skips_past_due(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    today = date.today()

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year - 1,
        opens_at=today - timedelta(days=400),
        closes_at=today - timedelta(days=30),
    )

    assert get_active_window(form_def) is None


@pytest.mark.django_db
def test_get_active_window_returns_none_when_no_window(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    SubmissionWindow.objects.filter(form_definition=form_def).delete()

    assert get_active_window(form_def) is None


# ─── can_create_draft / can_submit_draft ─────────────────────────────────────


@pytest.mark.django_db
def test_can_create_draft_blocks_when_no_window(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    SubmissionWindow.objects.filter(form_definition=form_def).delete()

    allowed, reason, window = can_create_draft(form_def)
    assert not allowed
    assert "No open submission window" in reason
    assert window is None


@pytest.mark.django_db
def test_can_create_draft_allows_when_upcoming(seed_data):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    today = date.today()

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year + 1,
        opens_at=today + timedelta(days=30),
        closes_at=today + timedelta(days=60),
    )

    allowed, _, window = can_create_draft(form_def)
    assert allowed
    assert window is not None


@pytest.mark.django_db
def test_can_submit_draft_allows_legacy_entries(seed_data, create_user):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    org = create_user.org_memberships.first().organization
    entry = FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=create_user, fiscal_year=None
    )

    allowed, reason = can_submit_draft(entry)
    assert allowed
    assert reason == ""


@pytest.mark.django_db
def test_can_submit_draft_blocks_when_upcoming(seed_data, create_user):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    today = date.today()

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year + 1,
        opens_at=today + timedelta(days=30),
        closes_at=today + timedelta(days=60),
    )

    org = create_user.org_memberships.first().organization
    entry = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=today.year + 1,
    )

    allowed, reason = can_submit_draft(entry)
    assert not allowed
    assert "opens on" in reason


@pytest.mark.django_db
def test_can_submit_draft_allows_when_past_due(seed_data, create_user):
    """Existing drafts must remain submittable after the window closes."""
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    today = date.today()

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=today.year - 1,
        opens_at=today - timedelta(days=120),
        closes_at=today - timedelta(days=30),
    )

    org = create_user.org_memberships.first().organization
    entry = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=today.year - 1,
    )

    allowed, reason = can_submit_draft(entry)
    assert allowed
    assert reason == ""


# ─── close_stale_drafts / closed_without_acceptance ──────────────────────────


@pytest.mark.django_db
def test_close_stale_drafts_closes_prior_fy_drafts(seed_data, create_user):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    org = create_user.org_memberships.first().organization

    prior = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=2025,
        status=FormEntry.STATUS_DRAFT,
    )
    current = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=2026,
        version_number=2,
        status=FormEntry.STATUS_DRAFT,
    )

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    new_window = SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=2026,
        opens_at=date(2025, 7, 1),
        closes_at=date(2025, 9, 1),
    )

    closed = close_stale_drafts(new_window)
    assert closed == 1

    prior.refresh_from_db()
    current.refresh_from_db()
    assert prior.status == FormEntry.STATUS_CLOSED_WITHOUT_ACCEPTANCE
    assert current.status == FormEntry.STATUS_DRAFT


@pytest.mark.django_db
def test_close_stale_drafts_skips_submitted_and_legacy_entries(seed_data, create_user):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    org = create_user.org_memberships.first().organization

    submitted = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=2025,
        status=FormEntry.STATUS_SUBMITTED,
    )
    legacy = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=None,
        version_number=2,
        status=FormEntry.STATUS_DRAFT,
    )

    SubmissionWindow.objects.filter(form_definition=form_def).delete()
    new_window = SubmissionWindow.objects.create(
        form_definition=form_def,
        fiscal_year=2026,
        opens_at=date(2025, 7, 1),
        closes_at=date(2025, 9, 1),
    )

    closed = close_stale_drafts(new_window)
    assert closed == 0

    submitted.refresh_from_db()
    legacy.refresh_from_db()
    assert submitted.status == FormEntry.STATUS_SUBMITTED
    assert legacy.status == FormEntry.STATUS_DRAFT


@pytest.mark.django_db
def test_can_submit_draft_blocks_closed_without_acceptance(seed_data, create_user):
    form_def = FormDefinition.objects.first()
    assert form_def is not None
    org = create_user.org_memberships.first().organization

    entry = FormEntry.objects.create(
        form_definition=form_def,
        organization=org,
        created_by=create_user,
        fiscal_year=2025,
        status=FormEntry.STATUS_CLOSED_WITHOUT_ACCEPTANCE,
    )

    allowed, reason = can_submit_draft(entry)
    assert not allowed
    assert "fiscal year rolled over" in reason
