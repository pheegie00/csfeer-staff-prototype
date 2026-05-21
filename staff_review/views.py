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

import uuid

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from form_manager.models.forms import FormAuditDetail, FormAuditTrail, FormEntry
from staff_review.management.commands.seed_demo_data import stable_uuid
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

class InboxView(TemplateView):
    """Federal-staff submission inbox -- the landing screen."""

    template_name = "staff_review/inbox.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        active_status = self.request.GET.get("status", "My queue")
        active_form = self.request.GET.get("form", "All")
        active_region = self.request.GET.get("region", "All")
        active_state = self.request.GET.get("state", "All")
        active_view = self.request.GET.get("view", "table")  # table | kanban | card
        query = (self.request.GET.get("q") or "").strip().lower()

        rows = self._filter(SUBMISSIONS, active_status, active_form, active_region, active_state, query)
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

        ctx.update({
            "user": USER,
            "rows": rows,
            "total": len(SUBMISSIONS),
            "filtered_count": len(rows),
            "counts": counts,
            "tabs": tabs,
            "kanban_columns": kanban_columns,
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

class SubmissionDetailView(TemplateView):
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


class SubmissionSaveEditView(View):
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


class RationaleView(View):
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

class ReturnBuilderView(TemplateView):
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


class ReturnSendView(View):
    """POST handler: send the return.

    In production this would: change status to Returned, clear AO sig
    (CORE-43), create ReturnItem rows, send recipient email (CORE-42,042),
    write to audit trail. Here we just toast and redirect.
    """

    def post(self, request, sub_id):
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404()

        items = []
        # Form posts as: item-1-section, item-1-field, item-1-text, item-2-*, etc.
        # Look for all item indices that have text
        i = 1
        while True:
            text = request.POST.get(f"item-{i}-text", "").strip()
            if text:
                items.append({
                    "section": request.POST.get(f"item-{i}-section", "").strip(),
                    "field": request.POST.get(f"item-{i}-field", "").strip(),
                    "text": text,
                })
            elif i > 10 and not text:
                break
            i += 1
            if i > 50:  # safety
                break

        summary = request.POST.get("summary", "").strip()

        if not items:
            messages.error(request, "At least one review item is required.")
            return redirect(reverse("staff_review:return_builder", kwargs={"sub_id": sub_id}))

        # Clear session drafts
        request.session.pop(f"return_drafts_{sub_id}", None)
        request.session.modified = True

        messages.success(
            request,
            f"Returned to {sub['data']['org']['name']} with {len(items)} item{'s' if len(items) != 1 else ''}. AO signature cleared. (mock -- no real DB/email).",
        )
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


# ============================================================
# DETERMINATION
# ============================================================

class DeterminationView(TemplateView):
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


class DeterminationRecordView(View):
    """POST handler: record the determination, lock the submission."""

    def post(self, request, sub_id):
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404()

        outcome = request.POST.get("outcome")
        notes = request.POST.get("notes", "").strip()

        if outcome not in ("Accepted", "Closed"):
            messages.error(request, "Choose Accept or Close without acceptance.")
            return redirect(reverse("staff_review:determination", kwargs={"sub_id": sub_id}))

        if outcome == "Closed" and not notes:
            messages.error(request, "Notes are required when closing without acceptance.")
            return redirect(reverse("staff_review:determination", kwargs={"sub_id": sub_id}))

        action = "accepted" if outcome == "Accepted" else "closed without acceptance"
        messages.success(
            request,
            f"Submission {action} and locked. (mock -- no real DB write).",
        )
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


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
