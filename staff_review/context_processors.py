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
        assignments = list(user.program_assignments.select_related("program__office").all())
        if not assignments:
            return "Federal Staff"
        roles = {a.role for a in assignments}

        # If the user covers exactly ONE program, name the program. Otherwise
        # collapse to office codes -- this lets us distinguish a "CSBG-only"
        # admin from an "OCS-wide" admin in the header chip.
        programs = {a.program.code for a in assignments}
        offices = {a.program.office.code for a in assignments}
        if len(programs) == 1:
            scope_str = next(iter(programs))
        else:
            scope_str = "/".join(sorted(offices))

        if "admin" in roles:
            return f"{scope_str} Program Admin"
        if "auditor" in roles:
            return f"{scope_str} Auditor"
        return f"{scope_str} Reviewer"

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

    # Show the View-as dropdown if the request is allowed to impersonate:
    # either the current user is a superuser, OR they were the superuser
    # who initiated View-as earlier in this session (session flag).
    # Importing inside the function avoids a circular-import risk at app load.
    from staff_review.demo_views import _request_can_use_viewas, get_demo_personas
    can_view_as = _request_can_use_viewas(request)
    demo_personas = get_demo_personas() if can_view_as else []

    # Feature flags: exposed as a plain dict so templates can do
    # `{% if flags.help_section %}`. Lazy import to avoid pulling models
    # at module load.
    from staff_review.feature_flags import flags_enabled_map
    flags = flags_enabled_map()

    return {
        "staff_persona": persona,
        "demo_personas": demo_personas,
        "is_demo_admin": can_view_as,
        "flags": flags,
    }
