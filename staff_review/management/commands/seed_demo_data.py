"""seed_demo_data -- materialize the staff_review mock_data into real DB rows.

Idempotent: safe to re-run; uses deterministic UUIDs derived from mock IDs
(uuid5 with a fixed namespace) so the same mock submission always maps to
the same FormEntry row.

Creates:
- 4 State rows (OK, AZ, AK, ND) if missing
- 1 CoreUser (the demo Federal Staff reviewer "Maya Rodriguez") if missing
- 9 OrganizationProfile rows (one per mock submission) if missing
- 2 FormDefinition rows ('CSBG Model Tribal Plan' and 'CSBG Annual Report
  3.0 Tribal Short Form (Tribes)') if missing
- 9 FormEntry rows (one per mock submission) with .data populated
- FormReturn + FormReturnItem rows for submissions in Returned/InProgress
  status
- Determination fields populated on FormEntry for resolved submissions
- FormAuditTrail seed events for each submission's event log

Run:
    uv run python manage.py seed_demo_data

Or to wipe and re-seed:
    uv run python manage.py seed_demo_data --reset
"""

import uuid
from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from form_manager.constants import (
    CSBGAnnualReportForms,
    CSBGTribalPlanApplicationForms,
    FormFamilies,
)
from form_manager.models.forms import FormAuditDetail, FormAuditTrail, FormDefinition, FormEntry
from organizations.constants import RegionChoices
from organizations.models import OrganizationProfile, State
from staff_review import mock_data
from staff_review.models import FormReturn, FormReturnItem

User = get_user_model()

# Stable namespace so uuid5(NS, mock_id) is the same every run, every machine.
DEMO_NS = uuid.UUID("8c30b9ce-7c5a-5d2e-9f8e-deadbeef0001")

# Mock form_type -> (FormDefinition.name, FormDefinition.family)
FORM_TYPE_MAPPING = {
    "tribal-plan": (
        CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN.value,
        FormFamilies.CSBG_TRIBAL_PLAN_APPLICATION.value,
    ),
    "annual-report-short": (
        CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0_SHORT.value,
        FormFamilies.CSBG_ANNUAL_REPORT.value,
    ),
}

# Mock status -> FormEntry.status (extended choices)
STATUS_MAPPING = {
    "Submitted": "submitted",
    "In Progress": "in_progress",
    "Returned": "returned",
    "Accepted": "accepted",
    "Closed": "closed",
}

# State abbreviation -> ACF region (matches RegionChoices in organizations.constants)
STATE_REGION = {
    "OK": "Region 6",
    "AZ": "Region 9",
    "AK": "Region 10",
    "ND": "Region 8",
}


def stable_uuid(prefix, *parts):
    """Generate a deterministic UUID from prefix + parts. Same input = same UUID."""
    key = ":".join([prefix, *(str(p) for p in parts)])
    return uuid.uuid5(DEMO_NS, key)


def parse_iso(s):
    """Parse 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM' to timezone-aware datetime."""
    if not s:
        return None
    if len(s) == 10:
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return datetime.strptime(s[:16], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)


class Command(BaseCommand):
    help = "Seed staff_review demo data from mock_data.SUBMISSIONS into real DB rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo rows (FormEntry + dependents matching demo UUIDs) before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()

        with transaction.atomic():
            self._seed_states()
            staff_user = self._seed_staff_user()
            form_defs = self._seed_form_definitions()
            for sub in mock_data.SUBMISSIONS:
                self._seed_submission(sub, form_defs, staff_user)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(mock_data.SUBMISSIONS)} demo submissions (idempotent)."
        ))

    # --------------------------------------------------------------------
    # Seeding helpers
    # --------------------------------------------------------------------

    def _reset(self):
        """Delete demo rows by deterministic UUID. Safe wrt other data."""
        demo_ids = [stable_uuid("form_entry", s["id"]) for s in mock_data.SUBMISSIONS]
        deleted, _ = FormEntry.objects.filter(id__in=demo_ids).delete()
        self.stdout.write(self.style.WARNING(f"Reset: deleted {deleted} demo rows."))

    def _seed_states(self):
        for abbr, region in STATE_REGION.items():
            State.objects.get_or_create(code=abbr, defaults={"region": region})

    def _seed_staff_user(self):
        user = mock_data.USER
        u, created = User.objects.get_or_create(
            email=user["email"],
            defaults={
                "first_name": user["name"].split()[0],
                "last_name": user["name"].split()[-1],
                "is_staff": True,
                "is_active": True,
            },
        )
        if created:
            u.set_unusable_password()
            u.save()
        return u

    def _seed_form_definitions(self):
        defs = {}
        for form_type, (name, family) in FORM_TYPE_MAPPING.items():
            fd, _ = FormDefinition.objects.get_or_create(
                name=name,
                variant="1.0.0",
                defaults={
                    "family": family,
                    "description": f"Demo FormDefinition for {name}",
                    "schema": {},
                    "schema_class": "DemoFormSchema",
                    "is_active": True,
                },
            )
            defs[form_type] = fd
        return defs

    def _seed_submission(self, sub, form_defs, staff_user):
        sub_id = sub["id"]
        form_def = form_defs[sub["form_type"]]

        # Look up State by mock data's state abbr (or full name)
        state_str = sub["data"]["org"].get("state", "")
        state_abbr = self._state_abbr(state_str)
        state = State.objects.filter(code=state_abbr).first()
        if not state:
            # Fallback: pick first state we know of
            state = State.objects.first()

        # Organization (deterministic UUID per mock org name)
        org_id = stable_uuid("org", sub["data"]["org"]["name"])
        org, _ = OrganizationProfile.objects.get_or_create(
            id=org_id,
            defaults={
                "name": sub["data"]["org"]["name"],
                "address": "",
                "contact_email": sub["data"]["contact"]["email"],
                "contact_phone": sub["data"]["contact"]["phone"],
                "state": state,
            },
        )

        # FormEntry (deterministic UUID per mock submission)
        entry_id = stable_uuid("form_entry", sub_id)
        determination_outcome = None
        determination_notes = ""
        determined_at = None
        determined_by = None
        if sub.get("determination"):
            d = sub["determination"]
            determination_outcome = "accepted" if d["outcome"] == "Accepted" else "closed"
            determination_notes = d.get("notes", "")
            determined_at = parse_iso(d.get("when"))
            determined_by = staff_user

        entry, created = FormEntry.objects.update_or_create(
            id=entry_id,
            defaults={
                "form_definition": form_def,
                "organization": org,
                "created_by": staff_user,
                "data": sub["data"],
                "version_number": 1,
                "status": STATUS_MAPPING.get(sub["status"], "submitted"),
                "submitted_at": parse_iso(sub.get("submitted")),
                "locked": sub["status"] in ("Accepted", "Closed"),
                "is_archived": False,
                "determination_outcome": determination_outcome,
                "determination_notes": determination_notes,
                "determined_at": determined_at,
                "determined_by": determined_by,
            },
        )

        # FormReturns + FormReturnItems
        if sub.get("return_items"):
            ret_id = stable_uuid("return", sub_id)
            returned_at_val = parse_iso(sub.get("returned_at")) or datetime.now(timezone.utc)
            ret, _ = FormReturn.objects.update_or_create(
                id=ret_id,
                defaults={
                    "form_entry": entry,
                    "returned_by": staff_user,
                    "summary": sub.get("return_summary", ""),
                    "ao_signature_cleared": bool(sub["data"].get("ao", {}).get("cleared")),
                },
            )
            # update auto_now_add field via raw save
            FormReturn.objects.filter(id=ret_id).update(returned_at=returned_at_val)

            # Items
            for i, ri in enumerate(sub["return_items"], start=1):
                ri_id = stable_uuid("return_item", sub_id, ri["id"])
                ack = ri.get("ack")
                FormReturnItem.objects.update_or_create(
                    id=ri_id,
                    defaults={
                        "form_return": ret,
                        "section": ri.get("section_label", ""),
                        "field": ri.get("field_label", ""),
                        "text": ri.get("text", ""),
                        "order": i,
                        "acknowledged_by": staff_user if ack else None,
                        "acknowledged_at": parse_iso(ack.get("when")) if ack else None,
                        "acknowledgement_response": ack.get("response", "") if ack else "",
                    },
                )

        # FormAuditTrail seed events (from sub['events'])
        for evt in sub.get("events", []):
            when_val = parse_iso(evt.get("when"))
            # Use deterministic UUID per (sub_id, when, action)
            audit_id = stable_uuid("audit", sub_id, evt.get("when", ""), evt.get("action", ""))
            FormAuditTrail.objects.update_or_create(
                id=audit_id,
                defaults={
                    "form_entry": entry,
                    "user": staff_user if evt.get("who_role") == "Federal Staff" else None,
                    "action": self._normalize_action(evt.get("kind", "event")),
                    "notes": evt.get("action", "") + (" -- " + evt["notes"] if evt.get("notes") else ""),
                    "rationale": "",
                },
            )
            if when_val:
                FormAuditTrail.objects.filter(id=audit_id).update(created_at=when_val)

    def _state_abbr(self, state_str):
        full_to_abbr = {
            "Oklahoma": "OK", "Arizona": "AZ", "Alaska": "AK", "North Dakota": "ND",
        }
        if state_str in full_to_abbr:
            return full_to_abbr[state_str]
        return state_str[:2].upper()

    def _normalize_action(self, kind):
        mapping = {
            "submit": "submit",
            "return": "return",
            "accept": "accept",
            "close": "close",
            "edit": "edit_on_behalf",
            "sign": "sign",
            "ack": "ack_review_item",
            "create": "create",
            "view": "view",
        }
        return mapping.get(kind, "event")
