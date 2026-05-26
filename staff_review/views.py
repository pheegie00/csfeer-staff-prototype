"""Views for staff_review (production federal-staff workflow).

Phase 3 Step 1 wiring:
- Mock_data still provides initial seed shape, but read paths query
  the real DB (FormEntry / FormReturn / FormReturnItem) via get_submission_view().
- Rationale flow (CORE-167) writes to FormAuditTrail + FormAuditDetail
  and applies edits to FormEntry.data.
- Inbox + detail views fall back to mock_data only if the DB hasn't been
  seeded yet (e.g., fresh checkout before running `make seed-demo-data`).

Screens implemented in this module:
- Inbox (Table view only; Kanban/Card views still on backlog)
- Submission detail (review mode)
- Submission detail (edit-on-behalf mode)
- Return for revision builder
- Rationale flow (POST handler that finalizes edits-on-behalf)
- Determination flow (POST handler that locks submission)
"""

import csv
import uuid

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from form_manager.models.forms import FormAuditDetail, FormAuditTrail, FormDefinition, FormEntry
from staff_review.audit_models import SystemEvent
from staff_review.management.commands.seed_demo_data import stable_uuid
from staff_review.models import FormReturn, FormReturnItem
from staff_review.feature_flags import FeatureRequiredMixin
from staff_review.permissions import StaffRequiredMixin, staff_queryset_filter
from staff_review.mock_data import (
    FORM_DEFS,
    STATUS_META,
    SUBMISSIONS,
    USER,
    age_badge_class,
    counts_by_status,
    fmt_currency,
    get_submission,
    total_budget,
)


# ============================================================
# DB ↔ mock_data bridge
# ============================================================
#
# Demo state is stored in real DB rows (after running
# `uv run python manage.py seed_demo_data`). Until then, views fall back
# to in-memory mock_data so the app renders out-of-the-box.
#
# Each mock submission's stable id ('s1', 's2', ...) maps to a
# deterministic FormEntry UUID via stable_uuid("form_entry", sub_id).
#
# Phase 3 Step 2+ will remove the mock_data fallback once seeding is
# part of the local-dev setup script.

def get_db_entry(sub_id):
    """Return the real FormEntry for a mock sub_id, or None if not seeded."""
    try:
        return FormEntry.objects.select_related("organization", "form_definition", "determined_by").get(
            id=stable_uuid("form_entry", sub_id)
        )
    except FormEntry.DoesNotExist:
        return None


def apply_db_overlay(mock_sub):
    """Layer DB-applied edits + status changes onto a mock submission.

    If a real FormEntry exists for this sub_id, prefer its current
    `data`, `status`, and determination fields over the mock baseline.
    Mock data remains the source of structural fallbacks (events, contacts).
    """
    entry = get_db_entry(mock_sub["id"])
    if entry is None:
        return mock_sub  # not seeded -- show raw mock

    # Build a shallow copy of mock + overlay
    out = dict(mock_sub)
    out["data"] = entry.data or mock_sub["data"]
    # Reverse-map DB status to mock display strings
    db_to_mock_status = {
        "submitted": "Submitted",
        "in_progress": "In Progress",
        "returned": "Returned",
        "amended": "In Progress",
        "accepted": "Accepted",
        "closed": "Closed",
        "archived": "Closed",
        "draft": "Submitted",  # not normally seen on staff side
    }
    out["status"] = db_to_mock_status.get(entry.status, mock_sub["status"])
    out["_db_entry"] = entry  # so views can reference for audit-trail-driven event feed
    if entry.determination_outcome:
        out["determination"] = {
            "outcome": "Accepted" if entry.determination_outcome == "accepted" else "Closed without Acceptance",
            "when": entry.determined_at.strftime("%Y-%m-%d") if entry.determined_at else "",
            "by": entry.determined_by.email if entry.determined_by else "",
            "notes": entry.determination_notes,
        }
    return out


# ============================================================
# INBOX
# ============================================================

class InboxView(StaffRequiredMixin, TemplateView):
    """Federal-staff submission inbox -- the landing screen."""

    template_name = "staff_review/inbox.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Phase 6 Figma redesign: simplify to Active / Completed buckets.
        # Active = anything NOT yet resolved (Submitted / In Progress / Returned).
        # Completed = Accepted / Closed.
        bucket = self.request.GET.get("bucket", "active").lower()
        if bucket not in ("active", "completed"):
            bucket = "active"
        active_status = "Resolved" if bucket == "completed" else "My queue"

        active_form = self.request.GET.get("form") or "All"
        active_region = self.request.GET.get("region") or "All"
        active_org = self.request.GET.get("org") or "All"
        active_fy = self.request.GET.get("fy") or "All"
        active_state = self.request.GET.get("state", "All")
        active_view = self.request.GET.get("view", "table")  # legacy
        query = (self.request.GET.get("q") or "").strip().lower()

        rows = self._filter(SUBMISSIONS, active_status, active_form, active_region, active_state, query)
        # Bucket-level filter on org + fy from the new Figma filter row.
        if active_org and active_org != "All":
            rows = [r for r in rows if r["data"]["org"].get("name") == active_org]
        if active_fy and active_fy != "All":
            rows = [r for r in rows if (r.get("fy") or r["data"]["org"].get("fy")) == active_fy]
        rows = self._enrich(rows)

        counts = counts_by_status(SUBMISSIONS)
        # Pre-compose tabs with counts so templates don't need branching.
        tabs = [
            {"id": "My queue",    "label": "My queue",    "count": counts["my_queue"]},
            {"id": "All",         "label": "All",         "count": counts["all"]},
            {"id": "Submitted",   "label": "Submitted",   "count": counts["submitted"]},
            {"id": "In Progress", "label": "In Progress", "count": counts["in_progress"]},
            {"id": "Returned",    "label": "Returned",    "count": counts["returned"]},
            {"id": "Resolved",    "label": "Resolved",    "count": counts["resolved"]},
        ]

        # Kanban columns -- buckets of rows by status (matches prototype hifi-inbox.jsx).
        kanban_columns = [
            {"status": "Submitted",   "label": "Submitted",   "hint": "New, awaiting review",
             "rows": [r for r in rows if r["status"] == "Submitted"]},
            {"status": "In Progress", "label": "In Progress", "hint": "Recipient editing",
             "rows": [r for r in rows if r["status"] == "In Progress"]},
            {"status": "Returned",    "label": "Returned",    "hint": "Awaiting resubmit",
             "rows": [r for r in rows if r["status"] == "Returned"]},
            {"status": "Accepted",    "label": "Accepted",    "hint": "Locked -- resolved",
             "rows": [r for r in rows if r["status"] == "Accepted"]},
            {"status": "Closed",      "label": "Closed",      "hint": "Closed without acceptance",
             "rows": [r for r in rows if r["status"] == "Closed"]},
        ]

        # Phase 6 redesign: build dropdown option lists from the seeded data
        # so the Figma filter row (regions, organizations, forms, fiscal years)
        # always shows real values.
        organizations = sorted({s["data"]["org"]["name"] for s in SUBMISSIONS})
        fiscal_years = sorted({
            (s.get("fy") or s["data"]["org"].get("fy") or "")
            for s in SUBMISSIONS
            if (s.get("fy") or s["data"]["org"].get("fy"))
        })
        form_options = sorted({FORM_DEFS[s["form_type"]]["short"] for s in SUBMISSIONS})

        ctx.update({
            "user": USER,
            "rows": rows,
            "total": len(SUBMISSIONS),
            "filtered_count": len(rows),
            "counts": counts,
            "tabs": tabs,
            "kanban_columns": kanban_columns,
            # Phase 6 Figma redesign context
            "bucket": bucket,
            "active_org": active_org,
            "active_fy": active_fy,
            "organizations": organizations,
            "fiscal_years": fiscal_years,
            "form_options": form_options,
            # Legacy / existing
            "active_status": active_status,
            "active_form": active_form,
            "active_region": active_region,
            "active_state": active_state,
            "active_view": active_view,
            "query": query,
            "forms":   ["All", "Tribal Plan", "Annual Report (Short)"],
            "regions": ["All", "VI", "VIII", "IX", "X"],
            "states":  ["All", "AK", "AZ", "ND", "OK"],
        })
        return ctx

    @staticmethod
    def _filter(subs, status, form, region, state, query):
        open_set = {"Submitted", "In Progress", "Returned"}
        resolved_set = {"Accepted", "Closed"}
        out = []
        for s in subs:
            if status == "My queue" and s["status"] not in open_set: continue
            elif status == "Resolved" and s["status"] not in resolved_set: continue
            elif status not in ("All", "My queue", "Resolved") and s["status"] != status: continue
            if form != "All" and FORM_DEFS[s["form_type"]]["short"] != form: continue
            org = s["data"]["org"]
            if region != "All" and org["region"] != region: continue
            if state != "All" and org["state"][:2].upper() != state and org.get("state") != _state_full(state):
                # Allow either abbreviation or full state name match
                continue
            if query and query not in org["name"].lower() and query not in org["uei"].lower():
                continue
            out.append(s)
        out.sort(key=lambda s: s["days_in"], reverse=True)
        return out

    @staticmethod
    def _enrich(rows):
        for s in rows:
            org = s["data"]["org"]
            s["form_short"] = FORM_DEFS[s["form_type"]]["short"]
            s["status_meta"] = STATUS_META.get(s["status"], STATUS_META["Submitted"])
            s["age_class"] = age_badge_class(s["days_in"], s["status"])
            s["returns_variant"] = "warning" if s["returns"] > 0 else "neutral"
            s["org_name"] = org["name"]
            s["uei"] = org["uei"]
            s["region"] = org["region"]
            s["state_abbr"] = _abbr(org["state"])
        return rows


def _state_full(abbr):
    return {"AK": "Alaska", "AZ": "Arizona", "ND": "North Dakota", "OK": "Oklahoma"}.get(abbr, abbr)


def _abbr(state):
    if not state:
        return ""
    if len(state) == 2:
        return state.upper()
    return {"Alaska": "AK", "Arizona": "AZ", "North Dakota": "ND", "Oklahoma": "OK"}.get(state, state[:2].upper())


# ============================================================
# SUBMISSION DETAIL (review + edit-on-behalf)
# ============================================================

class SubmissionDetailView(StaffRequiredMixin, TemplateView):
    """Submission detail. mode is 'review' (default) or 'edit'."""

    template_name = "staff_review/submission_detail.html"
    mode = "review"

    def get_context_data(self, **kwargs):
        sub_id = kwargs.get("sub_id")
        mock_sub = get_submission(sub_id)
        if mock_sub is None:
            raise Http404(f"Submission {sub_id} not found")

        # Overlay DB-applied edits + status changes on the mock baseline.
        # After CORE-167 rationale save, the form .data + .status reflect
        # what was persisted, not the mock_data starting point.
        sub = apply_db_overlay(mock_sub)

        ctx = super().get_context_data(**kwargs)
        d = sub["data"]
        fd = FORM_DEFS[sub["form_type"]]
        resolved = sub["status"] in ("Accepted", "Closed")
        returned = sub["status"] == "Returned"
        can_edit = not resolved and not returned
        can_return = not resolved and sub["returns"] == 0 and sub["status"] == "Submitted"
        can_determine = not resolved and sub["status"] in ("Submitted", "In Progress")
        final_review_only = sub["returns"] == 1 and not resolved and not returned

        # Pull pending edits from session for this submission
        session_key = f"pending_edits_{sub_id}"
        pending = self.request.session.get(session_key, {})

        # In edit mode, present a list of (path, original, current) for the rail
        pending_count = len(pending)

        ctx.update({
            "user": USER,
            "sub": sub,
            "d": d,
            "fd": fd,
            "mode": self.mode,
            "resolved": resolved,
            "returned": returned,
            "can_edit": can_edit,
            "can_return": can_return,
            "can_determine": can_determine,
            "final_review_only": final_review_only,
            "pending": pending,
            "pending_count": pending_count,
            "has_pending": pending_count > 0,
            "ack_count": sum(1 for r in sub["return_items"] if r.get("ack")),
            "total_budget": fmt_currency(total_budget(d["budget"])) if d.get("budget") else None,
            "status_meta": STATUS_META.get(sub["status"], STATUS_META["Submitted"]),
        })
        return ctx


class SubmissionEditView(SubmissionDetailView):
    """Edit-on-behalf mode. Same template, different mode flag."""
    mode = "edit"


class SubmissionSaveEditView(StaffRequiredMixin, View):
    """POST handler: accept inline form data, store in session as pending edits.

    Triggered when staff submit the edit form (NOT the rationale form).
    Stores changes in session and redirects back to edit page where the
    rail shows the pending edits and a 'Save with rationale' button.
    """

    def post(self, request, sub_id):
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404()

        # Fields that can be edited (paths from React TribalPlanForm + AnnualReportShortForm)
        editable = self._editable_paths(sub["form_type"])
        pending = {}
        for path in editable:
            # Form inputs use dotted path as the name attr (see
            # _form_tribal_plan.html); match that exactly.
            new_val = request.POST.get(path, None)
            if new_val is None:
                continue
            original = _get_by_path(sub["data"], path)
            # Coerce numbers for currency / outcomes fields
            if path.startswith("budget.") or path.startswith("outcomes."):
                try:
                    new_val = int(float(new_val.replace("$", "").replace(",", "").strip())) if new_val else original
                except (ValueError, AttributeError):
                    pass
            if str(new_val).strip() != str(original).strip():
                pending[path] = {"value": new_val, "original": original}

        session_key = f"pending_edits_{sub_id}"
        request.session[session_key] = pending
        request.session.modified = True

        if pending:
            messages.info(request, f"{len(pending)} pending edit(s) staged. Add a rationale to save.")
        else:
            messages.info(request, "No changes detected.")

        return redirect(reverse("staff_review:submission_edit", kwargs={"sub_id": sub_id}))

    @staticmethod
    def _editable_paths(form_type):
        if form_type == "tribal-plan":
            return [
                "contact.name", "contact.title", "contact.email", "contact.phone",
                "plan.mission", "plan.goals", "plan.coordination",
                "services",
                "budget.employment", "budget.education", "budget.emergency",
                "budget.housing", "budget.nutrition", "budget.admin", "budget.other",
                "narrative.employment", "narrative.housing", "narrative.emergency",
            ]
        else:
            return [
                "contact.name", "contact.title", "contact.email", "contact.phone",
                "period.start", "period.end",
                "outcomes.individualsServed", "outcomes.householdsServed",
                "outcomes.employment", "outcomes.education",
                "outcomes.housingStabilized", "outcomes.foodSecurity",
                "services",
            ]


class RationaleView(StaffRequiredMixin, View):
    """POST handler: finalize pending edits with a required rationale.

    Writes a real FormAuditTrail row (action='edit_on_behalf',
    rationale=<text>, user=<staff>) plus one FormAuditDetail child row
    per changed field (old + new value). Also applies the edits to
    FormEntry.data so the next view of the submission reflects them.

    CORE-167 (Add rationale when editing on a recipient's behalf):
        - rationale required (block save otherwise)
        - rationale + field changes stored on the audit trail
        - audit trail immutable once written

    Status transition: if the FormEntry was 'submitted', flips to
    'amended' (Federal Staff has touched it; AO re-signature gate
    applies before recipient can re-submit).
    """

    def post(self, request, sub_id):
        # Verify mock baseline exists (URL safety)
        mock_sub = get_submission(sub_id)
        if mock_sub is None:
            raise Http404()

        rationale = (request.POST.get("rationale") or "").strip()
        if not rationale:
            messages.error(request, "Rationale is required.")
            return redirect(reverse("staff_review:submission_edit", kwargs={"sub_id": sub_id}))

        session_key = f"pending_edits_{sub_id}"
        pending = request.session.get(session_key, {})
        n = len(pending)
        if n == 0:
            messages.warning(request, "No pending edits to save.")
            return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))

        # Look up the real FormEntry. If not seeded, error out clearly --
        # demo data must be present for CORE-167 wiring to function.
        entry = get_db_entry(sub_id)
        if entry is None:
            messages.error(
                request,
                "Database not seeded. Run `uv run python manage.py seed_demo_data` "
                "from the repo root, then retry.",
            )
            return redirect(reverse("staff_review:submission_edit", kwargs={"sub_id": sub_id}))

        actor = request.user if request.user.is_authenticated else None

        # Write the audit trail + field details + apply edits atomically.
        from django.db import transaction
        with transaction.atomic():
            trail = FormAuditTrail.objects.create(
                form_entry=entry,
                user=actor,
                action="edit_on_behalf",
                notes=f"Edited {n} field{'s' if n != 1 else ''} on behalf of {entry.organization.name}",
                rationale=rationale,
            )

            updated_data = dict(entry.data or {})
            for path, change in pending.items():
                new_val = change.get("value")
                old_val = change.get("original")

                FormAuditDetail.objects.create(
                    form_entry=entry,
                    user=actor,
                    field_name=path,
                    old_value=str(old_val) if old_val is not None else "",
                    new_value=str(new_val) if new_val is not None else "",
                )
                _set_by_path(updated_data, path, new_val)

            entry.data = updated_data
            # Transition status if appropriate (mirrors prototype behavior)
            if entry.status == "submitted":
                entry.status = "amended"
            entry.save(update_fields=["data", "status", "updated_at"])

        # Clear session staging
        request.session[session_key] = {}
        request.session.modified = True

        messages.success(
            request,
            f"{n} edit{'s' if n != 1 else ''} saved with rationale. "
            f"Audit trail row {trail.id} created.",
        )
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


def _set_by_path(obj, path, value):
    """In-place dotted-path setter on nested dict (mirrors hifi-detail.jsx setByPath)."""
    keys = path.split(".")
    cur = obj
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value


# ============================================================
# RETURN FOR REVISION BUILDER
# ============================================================

class ReturnBuilderView(StaffRequiredMixin, TemplateView):
    template_name = "staff_review/return_builder.html"

    def get_context_data(self, **kwargs):
        sub_id = kwargs.get("sub_id")
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404()

        ctx = super().get_context_data(**kwargs)
        fd = FORM_DEFS[sub["form_type"]]

        # Sections available as a "location" for review items (skip staff-locked sections)
        sections = [
            f'{s["num"]}. {s["title"]}' for s in fd["sections"] if not s.get("staff_locked")
        ]

        # Item drafts pulled from session (so user can build up items)
        drafts = self.request.session.get(f"return_drafts_{sub_id}", [{"id": 1, "section": "", "field": "", "text": ""}])

        ctx.update({
            "user": USER,
            "sub": sub,
            "fd": fd,
            "sections": sections,
            "drafts": drafts,
            "can_return": sub["status"] == "Submitted" and sub["returns"] == 0,
        })
        return ctx


class ReturnSendView(StaffRequiredMixin, View):
    """POST handler: send the return.

    Wires:
      CORE-168 -- write FormReturn + N FormReturnItem rows
      CORE-169 -- enforce one return per submission (block if already returned)
      CORE-43  -- clear AO signature on FormEntry.data.ao
      CORE-170 -- snapshot original submission into FormEntry.data['__original']
                  before any future resubmit-side mutations
      CORE-36  -- write FormAuditTrail row with action='return'

    Email notifications (CORE-42, CORE-41) are NOT sent here -- they
    depend on the email infrastructure SPIKE (CORE-70). Audit trail
    notes call this out for future wiring.
    """

    def post(self, request, sub_id):
        mock_sub = get_submission(sub_id)
        if mock_sub is None:
            raise Http404()

        # Collect items from form
        items = []
        i = 1
        while i <= 50:  # bounded
            text = request.POST.get(f"item-{i}-text", "").strip()
            if text:
                items.append({
                    "section": request.POST.get(f"item-{i}-section", "").strip(),
                    "field": request.POST.get(f"item-{i}-field", "").strip(),
                    "text": text,
                })
            i += 1

        summary = request.POST.get("summary", "").strip()

        if not items:
            messages.error(request, "At least one review item is required (CORE-168).")
            return redirect(reverse("staff_review:return_builder", kwargs={"sub_id": sub_id}))

        entry = get_db_entry(sub_id)
        if entry is None:
            messages.error(request, "Database not seeded. Run `make seed-demo-data` first.")
            return redirect(reverse("staff_review:return_builder", kwargs={"sub_id": sub_id}))

        # CORE-169: enforce one return per submission lifetime
        if entry.staff_returns.exists():
            messages.error(
                request,
                f"CORE-169: {entry.organization.name} has already been returned "
                f"once -- the only remaining actions are Accept or Close without Acceptance.",
            )
            return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))

        # CORE-45 / locked submissions cannot be returned
        if entry.locked or entry.status in ("accepted", "closed"):
            messages.error(request, "Submission is locked -- cannot return.")
            return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))

        actor = request.user if request.user.is_authenticated else None
        had_ao = bool((entry.data or {}).get("ao"))

        from django.db import transaction
        with transaction.atomic():
            # CORE-170: preserve a snapshot of the current submission state
            # under data['__original'] so resubmits can show what changed.
            # Only snapshot if not already snapshotted (preserve FIRST submission).
            data = dict(entry.data or {})
            if "__original" not in data:
                # Strip nested __original key if any (defensive)
                snapshot = {k: v for k, v in data.items() if k != "__original"}
                data["__original"] = snapshot

            # CORE-43: clear AO signature so AO must re-sign before resubmit
            ao_cleared = False
            if had_ao:
                ao = dict(data.get("ao") or {})
                ao["signed"] = False
                ao["cleared"] = True
                ao["clearedAt"] = timezone.now().strftime("%Y-%m-%d")
                data["ao"] = ao
                ao_cleared = True

            # CORE-168: create the FormReturn row
            ret = FormReturn.objects.create(
                form_entry=entry,
                returned_by=actor,
                summary=summary,
                ao_signature_cleared=ao_cleared,
            )

            # CORE-168: create one FormReturnItem per review item
            for idx, it in enumerate(items, start=1):
                FormReturnItem.objects.create(
                    form_return=ret,
                    section=it["section"],
                    field=it["field"],
                    text=it["text"],
                    order=idx,
                )

            # Transition status; clear AO; persist data snapshot
            entry.status = "returned"
            entry.data = data
            entry.save(update_fields=["status", "data", "updated_at"])

            # CORE-36: write audit trail
            FormAuditTrail.objects.create(
                form_entry=entry,
                user=actor,
                action="return",
                notes=(
                    f"Returned with {len(items)} review item{'s' if len(items) != 1 else ''} (CORE-168). "
                    + ("AO signature cleared (CORE-43). " if ao_cleared else "")
                    + "Recipient notification not yet wired (CORE-42 depends on SPIKE CORE-70). "
                    + "Original submission snapshot preserved (CORE-170)."
                ),
            )

        request.session.pop(f"return_drafts_{sub_id}", None)
        request.session.modified = True

        toast = (
            f"Returned to {entry.organization.name} with {len(items)} "
            f"item{'s' if len(items) != 1 else ''}. "
            + ("AO signature cleared. " if ao_cleared else "")
            + "Audit trail written. (Email notification still mocked.)"
        )
        messages.success(request, toast)
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


# ============================================================
# DETERMINATION
# ============================================================

class DeterminationView(StaffRequiredMixin, TemplateView):
    """Determination form (Accept / Close without acceptance + notes)."""

    template_name = "staff_review/determination.html"

    def get_context_data(self, **kwargs):
        sub_id = kwargs.get("sub_id")
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404()
        ctx = super().get_context_data(**kwargs)
        fd = FORM_DEFS[sub["form_type"]]
        ctx.update({
            "user": USER,
            "sub": sub,
            "fd": fd,
        })
        return ctx


class DeterminationRecordView(StaffRequiredMixin, View):
    """POST handler: record the determination, lock the submission.

    Wires:
      CORE-44 -- write determination_outcome, determination_notes,
                 determined_at, determined_by on FormEntry; transition
                 status to 'accepted' or 'closed'
      CORE-45 -- set FormEntry.locked = True (permanent compliance lock)
      CORE-36 -- write FormAuditTrail action='accept' or 'close'

    Once recorded, the submission is read-only at the application
    layer. Reverting requires DB intervention.
    """

    def post(self, request, sub_id):
        mock_sub = get_submission(sub_id)
        if mock_sub is None:
            raise Http404()

        outcome = request.POST.get("outcome")  # "Accepted" | "Closed"
        notes = request.POST.get("notes", "").strip()

        if outcome not in ("Accepted", "Closed"):
            messages.error(request, "Choose Accept or Close without acceptance.")
            return redirect(reverse("staff_review:determination", kwargs={"sub_id": sub_id}))

        if outcome == "Closed" and not notes:
            messages.error(request, "Notes are required when closing without acceptance.")
            return redirect(reverse("staff_review:determination", kwargs={"sub_id": sub_id}))

        entry = get_db_entry(sub_id)
        if entry is None:
            messages.error(request, "Database not seeded. Run `make seed-demo-data` first.")
            return redirect(reverse("staff_review:determination", kwargs={"sub_id": sub_id}))

        # CORE-45: cannot re-determine an already-resolved submission
        if entry.is_resolved or entry.locked:
            messages.error(
                request,
                f"CORE-45: Submission already resolved ({entry.get_status_display()}) "
                f"and locked from edits. Cannot re-determine.",
            )
            return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))

        actor = request.user if request.user.is_authenticated else None
        outcome_code = "accepted" if outcome == "Accepted" else "closed"
        action_label = "accept" if outcome == "Accepted" else "close"

        from django.db import transaction
        with transaction.atomic():
            # CORE-44: persist the determination
            entry.determination_outcome = outcome_code
            entry.determination_notes = notes
            entry.determined_at = timezone.now()
            entry.determined_by = actor
            entry.status = outcome_code

            # CORE-45: lock the submission permanently at the app layer
            entry.locked = True

            entry.save(update_fields=[
                "determination_outcome", "determination_notes",
                "determined_at", "determined_by",
                "status", "locked", "updated_at",
            ])

            # CORE-36: audit trail
            FormAuditTrail.objects.create(
                form_entry=entry,
                user=actor,
                action=action_label,
                notes=(
                    f"Final determination: {outcome} (CORE-44). "
                    f"Submission locked (CORE-45)."
                    + (f" Reviewer notes: {notes}" if notes else "")
                ),
            )

        verb = "accepted" if outcome == "Accepted" else "closed without acceptance"
        messages.success(
            request,
            f"Submission {verb} and locked. Audit trail written. "
            f"(Recipient + leadership notifications still mocked -- depends on CORE-70 SPIKE.)",
        )
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


# ============================================================
# CSV EXPORT (CORE-46)
# ============================================================
#
# Federal Staff must be able to export resolved submission data as
# structured CSV scoped to a specific form type from all organizations
# for a specific fiscal year. Export covers resolved submissions
# only (status = accepted or closed). Field names human-readable +
# consistent across exports.


class ExportsIndexView(FeatureRequiredMixin, StaffRequiredMixin, TemplateView):
    feature_key = "csv_exports"
    """Form to configure a CSV export.

    Lists distinct (form_definition, fiscal_year) combinations available
    for resolved-only export, plus the legend telling the user what's
    in scope. Submitting the form GETs the CSVExportView with query
    params.
    """

    template_name = "staff_review/exports.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        resolved = FormEntry.objects.filter(status__in=("accepted", "closed"))
        # Build pickers: distinct form definitions in resolved set
        form_defs = (
            FormDefinition.objects
            .filter(pk__in=resolved.values_list("form_definition_id", flat=True).distinct())
            .order_by("name")
        )
        # Fiscal years are in FormEntry.data['org']['fy'] -- collect distinct values
        fiscal_years = sorted({e.data.get("org", {}).get("fy", "") for e in resolved if e.data}, reverse=True)
        ctx.update({
            "user": USER,
            "form_defs": form_defs,
            "fiscal_years": [fy for fy in fiscal_years if fy],
            "resolved_count": resolved.count(),
        })
        return ctx


class CSVExportView(FeatureRequiredMixin, StaffRequiredMixin, View):
    feature_key = "csv_exports"

    """Generate + stream a CSV file. CORE-46.

    Required query params:
        form_type   -- FormDefinition.id (UUID)
        fy          -- fiscal year string, e.g. 'FY26'

    Returns text/csv with Content-Disposition: attachment.
    """

    def get(self, request):
        form_def_id = request.GET.get("form_type")
        fy = request.GET.get("fy", "").strip()

        if not form_def_id or not fy:
            messages.error(request, "Pick a form type and fiscal year.")
            return redirect(reverse("staff_review:exports"))

        try:
            form_def = FormDefinition.objects.get(pk=form_def_id)
        except (FormDefinition.DoesNotExist, ValueError):
            messages.error(request, "Form definition not found.")
            return redirect(reverse("staff_review:exports"))

        # Resolved-only (per CORE-46), filtered by form + fy
        entries = FormEntry.objects.filter(
            form_definition=form_def,
            status__in=("accepted", "closed"),
        ).select_related("organization", "determined_by").order_by("determined_at")
        entries = [e for e in entries if (e.data or {}).get("org", {}).get("fy") == fy]

        # Stream CSV response
        resp = HttpResponse(content_type="text/csv")
        filename = f"core_export_{form_def.name.lower().replace(' ', '_')}_{fy}_resolved.csv"
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(resp)
        # Header row -- human-readable, consistent column names per CORE-46
        writer.writerow([
            "Submission ID",
            "Organization",
            "UEI",
            "State",
            "Region",
            "Form Type",
            "Form Version",
            "Fiscal Year",
            "Submitted At",
            "Determined At",
            "Determination Outcome",
            "Determined By",
            "Determination Notes",
            "Returns Used",
            "AO Signed",
            "AO Name",
            "Primary Contact",
            "Primary Contact Email",
            "Primary Contact Phone",
        ])

        for e in entries:
            d = e.data or {}
            org = d.get("org", {})
            ao = d.get("ao", {}) or {}
            contact = d.get("contact", {}) or {}
            writer.writerow([
                str(e.id),
                e.organization.name,
                org.get("uei", ""),
                org.get("state", ""),
                org.get("region", ""),
                form_def.name,
                str(form_def.variant),
                org.get("fy", ""),
                e.submitted_at.isoformat() if e.submitted_at else "",
                e.determined_at.isoformat() if e.determined_at else "",
                e.get_determination_outcome_display() if e.determination_outcome else "",
                e.determined_by.email if e.determined_by else "",
                e.determination_notes,
                e.staff_returns.count(),
                "yes" if ao.get("signed") else "no",
                ao.get("name", ""),
                contact.get("name", ""),
                contact.get("email", ""),
                contact.get("phone", ""),
            ])

        # CORE-36: log the export as a system event
        SystemEvent.objects.create(
            kind="export_csv",
            actor=request.user if request.user.is_authenticated else None,
            ip_address=(request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
                        or request.META.get("REMOTE_ADDR")),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
            detail={
                "form_definition_id": str(form_def.id),
                "form_name": form_def.name,
                "fiscal_year": fy,
                "row_count": len(entries),
            },
            notes=f"CSV export: {form_def.name} / {fy} -- {len(entries)} resolved row{'s' if len(entries) != 1 else ''}",
        )
        return resp


# ============================================================
# SYSTEM AUDIT LOG VIEWER (CORE-47)
# ============================================================
#
# FISMA / NIST SP 800-53 compliance requirement. Shows every form-level
# audit event with actor + timestamp + action + notes + rationale.
# Append-only on the DB side; this view is read-only.

class AuditLogView(FeatureRequiredMixin, StaffRequiredMixin, TemplateView):
    feature_key = "audit_log_viewer"

    """System-wide audit log viewer.

    Filters: actor email, action type, organization, date range.
    Pagination: 50 rows per page.
    """

    template_name = "staff_review/audit_log.html"
    PAGE_SIZE = 50

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        actor = (self.request.GET.get("actor") or "").strip().lower()
        action = (self.request.GET.get("action") or "").strip()
        org_query = (self.request.GET.get("org") or "").strip().lower()
        page = max(1, int(self.request.GET.get("page", 1)))

        qs = FormAuditTrail.objects.select_related(
            "form_entry", "form_entry__organization", "user"
        ).order_by("-created_at")

        if actor:
            qs = qs.filter(user__email__icontains=actor)
        if action:
            qs = qs.filter(action=action)
        if org_query:
            qs = qs.filter(form_entry__organization__name__icontains=org_query)

        total = qs.count()
        start = (page - 1) * self.PAGE_SIZE
        rows = list(qs[start:start + self.PAGE_SIZE])

        # Available action types (for the dropdown)
        action_types = sorted(set(FormAuditTrail.objects.values_list("action", flat=True).distinct()))

        ctx.update({
            "user": USER,
            "rows": rows,
            "total": total,
            "page": page,
            "page_size": self.PAGE_SIZE,
            "page_count": (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE,
            "actor": actor,
            "active_action": action,
            "org_query": org_query,
            "action_types": action_types,
        })
        return ctx


# ============================================================
# Helpers
# ============================================================

def _get_by_path(obj, path):
    cur = obj
    for k in path.split("."):
        if cur is None:
            return None
        cur = cur.get(k) if isinstance(cur, dict) else None
    return cur
