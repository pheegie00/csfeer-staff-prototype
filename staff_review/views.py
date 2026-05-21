"""Views for staff_review (production federal-staff workflow).

Phase 2 translation of the React handoff bundle into Django + USWDS.
Mock data lives in staff_review.mock_data; Phase 3 replaces it with
real Submission querysets.

Screens implemented in this module:
- Inbox (Table view only; Kanban/Card views are next)
- Submission detail (review mode)
- Submission detail (edit-on-behalf mode)
- Return for revision builder
- Rationale flow (POST handler that finalizes edits-on-behalf)
- Determination flow (POST handler that locks submission)
"""

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

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
        query = (self.request.GET.get("q") or "").strip().lower()

        rows = self._filter(SUBMISSIONS, active_status, active_form, active_region, active_state, query)
        rows = self._enrich(rows)

        ctx.update({
            "user": USER,
            "rows": rows,
            "total": len(SUBMISSIONS),
            "filtered_count": len(rows),
            "counts": counts_by_status(SUBMISSIONS),
            "tabs": [
                ("My queue",    "My queue"),
                ("All",         "All"),
                ("Submitted",   "Submitted"),
                ("In Progress", "In Progress"),
                ("Returned",    "Returned"),
                ("Resolved",    "Resolved"),
            ],
            "active_status": active_status,
            "active_form": active_form,
            "active_region": active_region,
            "active_state": active_state,
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
        sub = get_submission(sub_id)
        if sub is None:
            raise Http404(f"Submission {sub_id} not found")

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
            field_name = path.replace(".", "__")
            new_val = request.POST.get(field_name, None)
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
    """POST handler: finalize the pending edits with a required rationale.

    In production this would write to FormAuditTrail per REQ-043 and
    update the Submission model. Here we just clear the session pending
    edits and toast.
    """

    def post(self, request, sub_id):
        sub = get_submission(sub_id)
        if sub is None:
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

        # Clear session pending; in real impl would persist to DB w/ rationale
        request.session[session_key] = {}
        request.session.modified = True
        messages.success(
            request,
            f"{n} edit{'s' if n != 1 else ''} saved with rationale. Logged (mock -- no real DB write yet).",
        )
        return redirect(reverse("staff_review:submission_detail", kwargs={"sub_id": sub_id}))


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
    (REQ-042), create ReturnItem rows, send recipient email (REQ-041,042),
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
