"""Template context processors for staff_review.

Exposes:
  staff_persona     -- a dict describing the currently logged-in user
                       for the header avatar / nav (name, initials,
                       role label, programs covered).
  demo_personas     -- a list of impersonable demo personas (superusers
                       only) so the View-as dropdown can render.
  is_demo_admin     -- bool, True if the current user can use the
                       View-as toggle.
"""

from staff_review.permissions import FEDERAL_STAFF_GROUP


def _initials(first, last, email):
    if first and last:
        return (first[0] + last[0]).upper()
    if first:
        return first[:2].upper()
    return (email[:2] if email else "??").upper()


def _role_label(user):
    """Best-guess role label for the header chip."""
    if not user.is_authenticated:
        return ""
    if user.is_superuser:
        return "Platform Superuser"

    # Staff side: read the highest-privilege role across their program assignments.
    if user.groups.filter(name=FEDERAL_STAFF_GROUP).exists():
        assignments = user.program_assignments.select_related("program__office").all()
        if not assignments:
            return "Federal Staff"
        roles = {a.role for a in assignments}
        # Office spans the assignments?
        offices = {a.program.office.code for a in assignments}
        office_str = "/".join(sorted(offices))
        if "admin" in roles:
            return f"{office_str} Program Admin"
        if "auditor" in roles:
            return f"{office_str} Auditor"
        return f"{office_str} Reviewer"

    # Recipient side: recipient groups are attached at
    # UserOrganizationMembership.groups (not user.groups directly). Union both.
    rec_groups = set(user.groups.values_list("name", flat=True))
    membership_group_names = user.org_memberships.values_list(
        "groups__name", flat=True,
    )
    rec_groups.update(g for g in membership_group_names if g)

    rec_order = [
        ("Recipient Authorized Official", "Authorized Official"),
        ("Recipient Form Approver", "Form Approver"),
        ("Recipient Form Editor", "Form Editor"),
        ("Recipient Form Viewer", "Form Viewer"),
    ]
    for group_name, label in rec_order:
        if group_name in rec_groups:
            return label
    return "User"


def staff_persona(request):
    """Header / nav context derived from request.user.

    The legacy views still pass a hardcoded `user` dict from
    mock_data.USER; this context processor adds a parallel
    `staff_persona` so the new nav doesn't depend on that.
    """
    u = getattr(request, "user", None)
    if u is None or not u.is_authenticated:
        return {
            "staff_persona": {
                "name": "Guest",
                "initials": "?",
                "email": "",
                "role_label": "",
                "is_authenticated": False,
            },
            "demo_personas": [],
            "is_demo_admin": False,
        }

    display_name = (
        (u.first_name + " " + u.last_name).strip()
        or u.email
        or "User"
    )
    persona = {
        "name": display_name,
        "initials": _initials(u.first_name, u.last_name, u.email),
        "email": u.email,
        "role_label": _role_label(u),
        "is_authenticated": True,
        "is_superuser": u.is_superuser,
    }

    # Only superusers see the View-as dropdown. Importing inside the
    # function avoids a circular-import risk at app load.
    if u.is_superuser:
        from staff_review.demo_views import get_demo_personas
        demo_personas = get_demo_personas()
    else:
        demo_personas = []

    return {
        "staff_persona": persona,
        "demo_personas": demo_personas,
        "is_demo_admin": u.is_superuser,
    }
