"""Mock submission data for staff_review screens.

Python port of staff_prototype/static/staff_prototype/hifi-data.js.
Used until real Submission models are wired in. Each screen view
imports this so designs render with the same data as the prototype.

Phase 3 (after model wiring): delete this file, replace imports with
Submission.objects queries.
"""

USER = {
    "id": "u1",
    "name": "Maya Rodriguez",
    "initials": "MR",
    "email": "m.rodriguez@acf.hhs.gov",
    "role": "Federal Staff",
    "org": "OCS Division of Community Assistance",
    "regions": ["VI", "IX", "X"],
}

FORM_DEFS = {
    "tribal-plan": {
        "name": "CSBG Tribal Plan & Application",
        "short": "Tribal Plan",
        "requires_ao": True,
        "omb": "0970-0635",
    },
    "annual-report-short": {
        "name": "CSBG Tribal Annual Report (Short Form)",
        "short": "Annual Report (Short)",
        "requires_ao": False,
        "omb": "0970-0492",
    },
}

# Status meta: USWDS-aligned tag variants
STATUS_META = {
    "Submitted":   {"variant": "info",    "hint": "Awaiting review"},
    "In Progress": {"variant": "warning", "hint": "Recipient editing"},
    "Returned":    {"variant": "warning", "hint": "Awaiting resubmit"},
    "Accepted":    {"variant": "success", "hint": "Locked"},
    "Closed":      {"variant": "neutral", "hint": "Locked"},
}

SUBMISSIONS = [
    {
        "id": "s1", "form_type": "tribal-plan", "status": "Submitted",
        "org_name": "Cherokee Nation", "uei": "QXYZ12AB34CD",
        "state": "OK", "region": "VI", "fy": "FY26",
        "submitted": "2026-04-12", "updated": "2026-05-18",
        "days_in": 9, "returns": 0,
        "primary_contact": {"name": "Sarah Whitewater", "title": "CSBG Program Director"},
    },
    {
        "id": "s2", "form_type": "tribal-plan", "status": "Returned",
        "org_name": "Navajo Nation", "uei": "NVJ8847LMNQ4",
        "state": "AZ", "region": "IX", "fy": "FY26",
        "submitted": "2026-04-08", "updated": "2026-05-15",
        "days_in": 13, "returns": 1,
        "primary_contact": {"name": "Marisol Begay", "title": "CSBG Program Director"},
    },
    {
        "id": "s3", "form_type": "annual-report-short", "status": "Submitted",
        "org_name": "Chickasaw Nation", "uei": "CKW7321ABCDE",
        "state": "OK", "region": "VI", "fy": "FY25",
        "submitted": "2026-04-15", "updated": "2026-05-19",
        "days_in": 6, "returns": 0,
        "primary_contact": {"name": "Rachel Anoatubby", "title": "Director of Community Services"},
    },
    {
        "id": "s4", "form_type": "tribal-plan", "status": "Accepted",
        "org_name": "Tanana Chiefs Conference", "uei": "TCC2200ZZAA9",
        "state": "AK", "region": "X", "fy": "FY26",
        "submitted": "2026-03-22", "updated": "2026-05-10",
        "days_in": 49, "returns": 1,
        "primary_contact": {"name": "Henry Solomon", "title": "Community Services Director"},
    },
    {
        "id": "s5", "form_type": "annual-report-short", "status": "Submitted",
        "org_name": "Hopi Tribe", "uei": "P4VR89LM21NK",
        "state": "AZ", "region": "IX", "fy": "FY25",
        "submitted": "2026-04-20", "updated": "2026-05-20",
        "days_in": 1, "returns": 0,
        "primary_contact": {"name": "Daniel Sekayumptewa", "title": "Community Services Director"},
    },
    {
        "id": "s6", "form_type": "tribal-plan", "status": "Submitted",
        "org_name": "Standing Rock Sioux Tribe", "uei": "SRS5566HJKLM",
        "state": "ND", "region": "VIII", "fy": "FY26",
        "submitted": "2026-04-02", "updated": "2026-05-17",
        "days_in": 19, "returns": 0,
        "primary_contact": {"name": "Joseph Brings Plenty", "title": "Tribal Administrator"},
    },
    {
        "id": "s7", "form_type": "tribal-plan", "status": "In Progress",
        "org_name": "Kawerak Inc.", "uei": "KWR4488POIUY",
        "state": "AK", "region": "X", "fy": "FY26",
        "submitted": "2026-03-30", "updated": "2026-05-19",
        "days_in": 22, "returns": 1,
        "primary_contact": {"name": "Lisa Ellanna", "title": "Director of Community Services"},
    },
    {
        "id": "s8", "form_type": "annual-report-short", "status": "Closed",
        "org_name": "Salt River Pima-Maricopa", "uei": "SRP8800GFEDC",
        "state": "AZ", "region": "IX", "fy": "FY25",
        "submitted": "2026-04-18", "updated": "2026-04-30",
        "days_in": 12, "returns": 0,
        "primary_contact": {"name": "Diane Enos", "title": "CS Coordinator"},
    },
    {
        "id": "s9", "form_type": "tribal-plan", "status": "Submitted",
        "org_name": "Choctaw Nation of Oklahoma", "uei": "CTW6677QRSTU",
        "state": "OK", "region": "VI", "fy": "FY26",
        "submitted": "2026-04-11", "updated": "2026-05-18",
        "days_in": 10, "returns": 0,
        "primary_contact": {"name": "Sara Bond", "title": "Community Services Manager"},
    },
]


def age_badge_class(days, status):
    """Match the React AgeBadge logic in hifi-workflow.jsx."""
    if status in ("Accepted", "Closed"):
        return "age-badge--neutral"
    if days >= 20:
        return "age-badge--hot"
    if days >= 10:
        return "age-badge--warm"
    return "age-badge--cool"


def counts_by_status(subs):
    """Tab counters for the toolbar."""
    open_set = {"Submitted", "In Progress", "Returned"}
    resolved_set = {"Accepted", "Closed"}
    return {
        "all": len(subs),
        "my_queue": sum(1 for s in subs if s["status"] in open_set),
        "submitted": sum(1 for s in subs if s["status"] == "Submitted"),
        "in_progress": sum(1 for s in subs if s["status"] == "In Progress"),
        "returned": sum(1 for s in subs if s["status"] == "Returned"),
        "resolved": sum(1 for s in subs if s["status"] in resolved_set),
    }
