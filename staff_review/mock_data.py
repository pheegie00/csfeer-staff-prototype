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
        "sections": [
            {"id": "org", "num": 1, "title": "Organization Information", "auto": True},
            {"id": "contact", "num": 2, "title": "Primary Contact"},
            {"id": "plan", "num": 3, "title": "Programmatic Plan"},
            {"id": "services", "num": 4, "title": "Service Areas"},
            {"id": "budget", "num": 5, "title": "Proposed Budget"},
            {"id": "narrative", "num": 6, "title": "Programmatic Narrative"},
            {"id": "attestation", "num": 7, "title": "Attestation of Assurances", "staff_locked": True},
            {"id": "ao", "num": 8, "title": "Authorized Official Signature", "staff_locked": True, "requires_ao": True},
        ],
    },
    "annual-report-short": {
        "name": "CSBG Tribal Annual Report (Short Form)",
        "short": "Annual Report (Short)",
        "requires_ao": False,
        "omb": "0970-0492",
        "sections": [
            {"id": "org", "num": 1, "title": "Organization Information", "auto": True},
            {"id": "contact", "num": 2, "title": "Primary Contact"},
            {"id": "period", "num": 3, "title": "Reporting Period"},
            {"id": "outcomes", "num": 4, "title": "Outcomes & Counts"},
            {"id": "services", "num": 5, "title": "Services Provided"},
            {"id": "attestation", "num": 6, "title": "Attestation", "staff_locked": True},
        ],
    },
}

STATUS_META = {
    "Submitted":   {"variant": "info",    "hint": "Awaiting review"},
    "In Progress": {"variant": "warning", "hint": "Recipient editing"},
    "Returned":    {"variant": "warning", "hint": "Awaiting resubmit"},
    "Accepted":    {"variant": "success", "hint": "Locked"},
    "Closed":      {"variant": "neutral", "hint": "Locked"},
}


def _plan_data(**overrides):
    base = {
        "org": {"name": "Cherokee Nation", "uei": "QXYZ12AB34CD", "duns": "073827234",
                "state": "Oklahoma", "region": "VI", "fy": "FY26"},
        "contact": {"name": "Sarah Whitewater", "title": "CSBG Program Director",
                    "email": "s.whitewater@cherokee.org", "phone": "(918) 453-5000"},
        "plan": {
            "mission": "Reduce poverty and increase self-sufficiency for Cherokee Nation citizens through coordinated, evidence-based programs.",
            "goals": "Maintain >=85% client satisfaction; place 200+ adults in employment; stabilize housing for 400+ households.",
            "coordination": "Coordination with Cherokee Nation Career Services, Education Services, and Health System ensures wraparound delivery.",
        },
        "services": "All 14 counties of the Cherokee Nation jurisdictional area, with priority for households below 125% FPL.",
        "budget": {"employment": 1250000, "education": 680000, "emergency": 945000,
                   "housing": 610000, "nutrition": 405000, "admin": 485000, "other": 515000},
        "narrative": {
            "employment": "Continue partnership with Cherokee Nation Career Services to provide job training, placement support, and supportive services.",
            "housing": "Eviction prevention, rapid rehousing, and tribal housing authority coordination.",
            "emergency": "Emergency food, utility, and shelter assistance through 7 satellite offices.",
        },
        "attestation": {"ackBy": "Sarah Whitewater", "ackAt": "2026-04-11"},
        "ao": {"name": "William Acornlee", "title": "Principal Chief",
               "email": "w.acornlee@cherokee.org", "signed": True, "signedAt": "2026-04-12",
               "cleared": False, "clearedAt": None},
    }
    for k, v in overrides.items():
        base[k] = v
    return base


def _report_data(**overrides):
    base = {
        "org": {"name": "Hopi Tribe", "uei": "P4VR89LM21NK", "state": "Arizona",
                "region": "IX", "fy": "FY25"},
        "contact": {"name": "Daniel Sekayumptewa", "title": "Community Services Director",
                    "email": "d.sekay@hopi-nsn.gov", "phone": "(928) 734-3000"},
        "period": {"start": "2024-10-01", "end": "2025-09-30"},
        "outcomes": {"individualsServed": 8420, "householdsServed": 2104, "employment": 89,
                     "education": 412, "housingStabilized": 187, "foodSecurity": 1240},
        "services": "Workforce development, emergency assistance, food box program, energy assistance navigation.",
        "attestation": {"ackBy": "Daniel Sekayumptewa", "ackAt": "2026-04-20"},
    }
    for k, v in overrides.items():
        base[k] = v
    return base


SUBMISSIONS = [
    {
        "id": "s1", "form_type": "tribal-plan", "status": "Submitted",
        "fy": "FY26", "submitted": "2026-04-12", "updated": "2026-05-18",
        "days_in": 9, "returns": 0,
        "data": _plan_data(),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-05-19 16:14", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Opened submission for review", "kind": "view"},
            {"when": "2026-05-18 09:02", "who": "Sarah Whitewater", "who_role": "Recipient Approver",
             "action": "Submitted form", "notes": "Submission timestamped. AO signature attached.", "kind": "submit"},
            {"when": "2026-05-18 09:01", "who": "William Acornlee", "who_role": "Authorized Official",
             "action": "Signed Authorized Official section", "kind": "sign"},
            {"when": "2026-04-12 08:30", "who": "Cody Davis", "who_role": "Recipient Contributor",
             "action": "Created draft", "kind": "create"},
        ],
    },
    {
        "id": "s2", "form_type": "tribal-plan", "status": "Returned",
        "fy": "FY26", "submitted": "2026-04-08", "updated": "2026-05-15",
        "days_in": 13, "returns": 1, "returned_at": "2026-05-08",
        "return_summary": "Thanks for the submission -- overall in good shape. Three items below to address. Reach out if any are unclear.",
        "data": _plan_data(
            org={"name": "Navajo Nation", "uei": "NVJ8847LMNQ4", "state": "Arizona", "region": "IX", "fy": "FY26"},
            contact={"name": "Marisol Begay", "title": "CSBG Program Director",
                     "email": "m.begay@navajo-nsn.gov", "phone": "(928) 871-5567"},
            ao={"name": "Buu Nygren", "title": "President, Navajo Nation",
                "email": "president@navajo-nsn.gov", "signed": False, "signedAt": None,
                "cleared": True, "clearedAt": "2026-05-08"},
            budget={"employment": 2840000, "education": 1560000, "emergency": 2120000,
                    "housing": 1450000, "nutrition": 920000, "admin": 720000, "other": 890000},
        ),
        "return_items": [
            {"id": "ri1", "section_label": "Section 2 - Primary Contact",
             "field_label": "Phone",
             "text": "Phone number on file appears outdated. Please confirm the current direct line for the Program Director -- the last quarterly review attempted contact and got a disconnected line.",
             "ack": {"by": "Marisol Begay", "when": "2026-05-12",
                     "response": "Confirmed -- new direct line is (928) 871-5567. Updated in form."}},
            {"id": "ri2", "section_label": "Section 5 - Proposed Budget",
             "field_label": "Administrative",
             "text": "Administrative line exceeds the 15% cap defined in 42 U.S.C. 9907(b)(1). Either reduce admin to <= $733,500 (15% of total) or provide written justification.",
             "ack": {"by": "Marisol Begay", "when": "2026-05-14",
                     "response": "Reduced admin to $720,000 (14.7%). Reallocated $25,000 to Emergency Assistance."}},
            {"id": "ri3", "section_label": "Section 6 - Programmatic Narrative",
             "field_label": "Employment Services narrative",
             "text": "Employment Services narrative does not describe the workforce partnership with Cherokee Nation Career Services referenced in your FY25 final report. Please add 2-3 sentences clarifying scope and target populations for FY26.",
             "ack": None},
        ],
        "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-05-14 11:02", "who": "Marisol Begay", "who_role": "Recipient Approver",
             "action": "Acknowledged review item 2", "kind": "ack"},
            {"when": "2026-05-12 14:18", "who": "Marisol Begay", "who_role": "Recipient Approver",
             "action": "Acknowledged review item 1", "kind": "ack"},
            {"when": "2026-05-08 10:30", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Returned submission - 3 items",
             "notes": "AO Signature cleared. Recipient notified.", "kind": "return"},
            {"when": "2026-04-08 14:22", "who": "Marisol Begay", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
            {"when": "2026-04-08 14:21", "who": "Buu Nygren", "who_role": "Authorized Official",
             "action": "Signed Authorized Official section", "kind": "sign"},
        ],
    },
    {
        "id": "s3", "form_type": "annual-report-short", "status": "Submitted",
        "fy": "FY25", "submitted": "2026-04-15", "updated": "2026-05-19",
        "days_in": 6, "returns": 0,
        "data": _report_data(
            org={"name": "Chickasaw Nation", "uei": "CKW7321ABCDE", "state": "Oklahoma", "region": "VI", "fy": "FY25"},
            contact={"name": "Rachel Anoatubby", "title": "Director of Community Services",
                     "email": "r.anoatubby@chickasaw.net", "phone": "(580) 421-7711"},
            outcomes={"individualsServed": 14200, "householdsServed": 3850, "employment": 142,
                      "education": 680, "housingStabilized": 310, "foodSecurity": 2180},
        ),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-04-15 11:00", "who": "Rachel Anoatubby", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s4", "form_type": "tribal-plan", "status": "Accepted",
        "fy": "FY26", "submitted": "2026-03-22", "updated": "2026-05-10",
        "days_in": 49, "returns": 1, "resolved": "2026-05-10",
        "data": _plan_data(
            org={"name": "Tanana Chiefs Conference", "uei": "TCC2200ZZAA9",
                 "state": "Alaska", "region": "X", "fy": "FY26"},
            contact={"name": "Henry Solomon", "title": "Community Services Director",
                     "email": "h.solomon@tananachiefs.org", "phone": "(907) 452-8251"},
            ao={"name": "Brian Ridley", "title": "Chief / Chairman",
                "email": "b.ridley@tananachiefs.org", "signed": True, "signedAt": "2026-05-02",
                "cleared": False, "clearedAt": None},
        ),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": {"outcome": "Accepted", "when": "2026-05-10", "by": "Maya Rodriguez",
                          "notes": "All review items resolved on resubmit. Budget revised to comply with 15% admin cap. AO re-signed 5/2."},
        "events": [
            {"when": "2026-05-10 15:48", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Accepted submission - final determination", "kind": "accept"},
            {"when": "2026-05-02 09:14", "who": "Henry Solomon", "who_role": "Recipient Approver",
             "action": "Resubmitted form", "kind": "submit"},
            {"when": "2026-05-02 09:12", "who": "Brian Ridley", "who_role": "Authorized Official",
             "action": "Re-signed Authorized Official section", "kind": "sign"},
            {"when": "2026-04-04 11:30", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Returned submission - 3 items", "kind": "return"},
            {"when": "2026-03-22 16:45", "who": "Henry Solomon", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s5", "form_type": "annual-report-short", "status": "Submitted",
        "fy": "FY25", "submitted": "2026-04-20", "updated": "2026-05-20",
        "days_in": 1, "returns": 0,
        "data": _report_data(),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-04-20 14:00", "who": "Daniel Sekayumptewa", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s6", "form_type": "tribal-plan", "status": "Submitted",
        "fy": "FY26", "submitted": "2026-04-02", "updated": "2026-05-17",
        "days_in": 19, "returns": 0,
        "data": _plan_data(
            org={"name": "Standing Rock Sioux Tribe", "uei": "SRS5566HJKLM",
                 "state": "North Dakota", "region": "VIII", "fy": "FY26"},
            contact={"name": "Joseph Brings Plenty", "title": "Tribal Administrator",
                     "email": "j.bringsplenty@srst.gov", "phone": "(701) 854-7203"},
            ao={"name": "Janet Alkire", "title": "Tribal Chairwoman",
                "email": "chair@srst.gov", "signed": True, "signedAt": "2026-04-02",
                "cleared": False, "clearedAt": None},
        ),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-04-02 10:15", "who": "Joseph Brings Plenty", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s7", "form_type": "tribal-plan", "status": "In Progress",
        "fy": "FY26", "submitted": "2026-03-30", "updated": "2026-05-19",
        "days_in": 22, "returns": 1, "returned_at": "2026-04-22",
        "data": _plan_data(
            org={"name": "Kawerak Inc.", "uei": "KWR4488POIUY",
                 "state": "Alaska", "region": "X", "fy": "FY26"},
            contact={"name": "Lisa Ellanna", "title": "Director of Community Services",
                     "email": "l.ellanna@kawerak.org", "phone": "(907) 443-5231"},
            ao={"name": "Melanie Bahnke", "title": "President / CEO",
                "email": "president@kawerak.org", "signed": False, "signedAt": None,
                "cleared": True, "clearedAt": "2026-04-22"},
        ),
        "return_items": [
            {"id": "kri1", "section_label": "Section 5 - Budget", "field_label": "Administrative",
             "text": "Admin allocation exceeds threshold.",
             "ack": {"by": "Lisa Ellanna", "when": "2026-05-12", "response": "Working on revised allocation."}},
        ],
        "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-05-19 15:00", "who": "Lisa Ellanna", "who_role": "Recipient Approver",
             "action": "Editing form", "kind": "edit"},
            {"when": "2026-04-22 09:30", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Returned submission - 1 item", "kind": "return"},
            {"when": "2026-03-30 11:00", "who": "Lisa Ellanna", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s8", "form_type": "annual-report-short", "status": "Closed",
        "fy": "FY25", "submitted": "2026-04-18", "updated": "2026-04-30",
        "days_in": 12, "returns": 0, "resolved": "2026-04-30",
        "data": _report_data(
            org={"name": "Salt River Pima-Maricopa", "uei": "SRP8800GFEDC",
                 "state": "Arizona", "region": "IX", "fy": "FY25"},
            contact={"name": "Diane Enos", "title": "CS Coordinator",
                     "email": "d.enos@srpmic-nsn.gov", "phone": "(480) 362-7740"},
        ),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": {"outcome": "Closed without Acceptance", "when": "2026-04-30",
                          "by": "Maya Rodriguez",
                          "notes": "Organization withdrew from FY25 reporting cycle due to merger with neighboring agency. Closed administratively at recipient request."},
        "events": [
            {"when": "2026-04-30 13:22", "who": "Maya Rodriguez", "who_role": "Federal Staff",
             "action": "Closed without acceptance", "kind": "close"},
            {"when": "2026-04-18 16:00", "who": "Diane Enos", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
    {
        "id": "s9", "form_type": "tribal-plan", "status": "Submitted",
        "fy": "FY26", "submitted": "2026-04-11", "updated": "2026-05-18",
        "days_in": 10, "returns": 0,
        "data": _plan_data(
            org={"name": "Choctaw Nation of Oklahoma", "uei": "CTW6677QRSTU",
                 "state": "Oklahoma", "region": "VI", "fy": "FY26"},
            contact={"name": "Sara Bond", "title": "Community Services Manager",
                     "email": "s.bond@choctawnation.com", "phone": "(580) 924-8280"},
            ao={"name": "Gary Batton", "title": "Chief, Choctaw Nation",
                "email": "chief@choctawnation.com", "signed": True, "signedAt": "2026-04-11",
                "cleared": False, "clearedAt": None},
        ),
        "return_items": [], "edits": [], "pending_edits": {},
        "determination": None,
        "events": [
            {"when": "2026-04-11 09:30", "who": "Sara Bond", "who_role": "Recipient Approver",
             "action": "Submitted form", "kind": "submit"},
        ],
    },
]


# ============================================================
# Helpers (mirror the React app)
# ============================================================

def get_submission(sub_id):
    for s in SUBMISSIONS:
        if s["id"] == sub_id:
            return s
    return None


def age_badge_class(days, status):
    if status in ("Accepted", "Closed"):
        return "age-badge--neutral"
    if days >= 20:
        return "age-badge--hot"
    if days >= 10:
        return "age-badge--warm"
    return "age-badge--cool"


def counts_by_status(subs):
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


def fmt_currency(n):
    if n is None or n == "":
        return "--"
    try:
        n = float(str(n).replace("$", "").replace(",", ""))
    except (ValueError, TypeError):
        return n
    if n == int(n):
        return "${:,}".format(int(n))
    return "${:,.2f}".format(n)


def total_budget(budget):
    return sum(v or 0 for v in budget.values())
