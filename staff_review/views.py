"""Views for staff_review (production federal-staff workflow).

Currently: Inbox screen only (Table view). Phase 2 expansion targets:
- Submission detail (review + edit-on-behalf modes)
- Return for revision builder
- Rationale modal (HTMX/standard form)
- Determination modal
"""

from django.views.generic import TemplateView

from staff_review.mock_data import (
    FORM_DEFS,
    STATUS_META,
    SUBMISSIONS,
    USER,
    age_badge_class,
    counts_by_status,
)


class InboxView(TemplateView):
    """Federal-staff submission inbox -- the landing screen.

    Translates hifi-inbox.jsx TableView to Django + USWDS Cotton.
    Kanban + Card views land in a follow-up commit.
    """

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
            if region != "All" and s["region"] != region: continue
            if state != "All" and s["state"] != state: continue
            if query and query not in s["org_name"].lower() and query not in s["uei"].lower():
                continue
            out.append(s)
        # default sort: days_in desc
        out.sort(key=lambda s: s["days_in"], reverse=True)
        return out

    @staticmethod
    def _enrich(rows):
        """Add presentation-only fields used by the template."""
        for s in rows:
            s["form_short"] = FORM_DEFS[s["form_type"]]["short"]
            s["status_meta"] = STATUS_META.get(s["status"], STATUS_META["Submitted"])
            s["age_class"] = age_badge_class(s["days_in"], s["status"])
            s["returns_variant"] = "warning" if s["returns"] > 0 else "neutral"
        return rows
