"""seed_demo_users -- materialize one sample user per role for testing/demo.

Phase 4 Step 7. Pairs with the View-as toggle in the staff nav so a
superuser can flip between personas with one click during demos and
testing.

Roles covered:
    Staff side (Federal Staff group + UserProgramAssignment):
      - maya.rodriguez@acf.hhs.gov  - OCS Reviewer (all OCS programs)
      - dana.chen@acf.hhs.gov       - OCS Program Admin (all OCS, admin role)
      - sam.patel@acf.hhs.gov       - OFA Program Admin (all OFA, admin role)
      - riley.brooks@acf.hhs.gov    - OCS Auditor  (all OCS, auditor role)
      - root@acf.hhs.gov            - Platform Superuser (cross-office)

    Recipient side (UserOrganizationMembership + Recipient* group):
      - tribe-ao@example.com        - Choctaw Nation Authorized Official
      - state-editor@example.com    - State of Oklahoma Form Editor
      - cbo-approver@example.com    - Test CBO Form Approver

Idempotent: safe to re-run; everything is get_or_create. Run as part
of `seed_demo_data` (called automatically) or standalone:

    uv run python manage.py seed_demo_users
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from organizations.models import (
    OrganizationProfile,
    OrgType,
    State,
    UserOrganizationMembership,
)
from programs.models import Program, UserProgramAssignment
from staff_review.permissions import FEDERAL_STAFF_GROUP
from users.permissions import (
    RECIPIENT_AUTHORIZED_OFFICIAL,
    RECIPIENT_FORM_APPROVER,
    RECIPIENT_FORM_EDITOR,
)

User = get_user_model()


# ---- Staff personas ---------------------------------------------------

# (email, first, last, scope, role, is_superuser, label)
#
# scope is one of:
#   "*"                  -- cross-office (superuser-style, all programs)
#   "OCS" / "OFA"        -- all programs under that office
#   ["CSBG", "LIHEAP"]   -- explicit list of program codes
#
# role values match UserProgramAssignment.ROLE_CHOICES.
STAFF_PERSONAS = [
    # Whole-office staff
    ("maya.rodriguez@acf.hhs.gov", "Maya", "Rodriguez", "OCS", "reviewer", False,
     "OCS Reviewer"),
    ("dana.chen@acf.hhs.gov", "Dana", "Chen", "OCS", "admin", False,
     "OCS Program Admin"),
    ("sam.patel@acf.hhs.gov", "Sam", "Patel", "OFA", "admin", False,
     "OFA Program Admin"),
    ("riley.brooks@acf.hhs.gov", "Riley", "Brooks", "OCS", "auditor", False,
     "OCS Auditor"),

    # Single-program admins -- narrower than whole-office
    ("jordan.lee@acf.hhs.gov", "Jordan", "Lee", ["CSBG"], "admin", False,
     "CSBG Program Admin"),
    ("casey.wu@acf.hhs.gov", "Casey", "Wu", ["LIHEAP"], "admin", False,
     "LIHEAP Program Admin"),

    # Cross-everything superuser
    ("root@acf.hhs.gov", "Platform", "Admin", "*", "admin", True,
     "Platform Superuser"),
]


# ---- Recipient personas ------------------------------------------------

# (email, first, last, org_name, org_type, state_code, group_name, label)
RECIPIENT_PERSONAS = [
    ("tribe-ao@example.com", "Tasha", "Whitehorse",
     "Choctaw Nation of Oklahoma (Demo)", OrgType.TRIBE, "OK",
     RECIPIENT_AUTHORIZED_OFFICIAL,
     "Tribe Authorized Official (CSBG)"),
    ("state-editor@example.com", "Jordan", "Miller",
     "Oklahoma Department of Commerce (Demo)", OrgType.STATE, "OK",
     RECIPIENT_FORM_EDITOR,
     "State Form Editor (LIHEAP/SSBG)"),
    ("cbo-approver@example.com", "Alex", "Nguyen",
     "Tulsa Community Action Agency (Demo)", OrgType.CBO, "OK",
     RECIPIENT_FORM_APPROVER,
     "CBO Form Approver (CED)"),
]


class Command(BaseCommand):
    help = "Seed sample users covering every staff + recipient role tier."

    def handle(self, *args, **options):
        with transaction.atomic():
            self._ensure_states()
            staff_group = self._ensure_federal_staff_group()
            for persona in STAFF_PERSONAS:
                self._seed_staff_persona(persona, staff_group)
            for persona in RECIPIENT_PERSONAS:
                self._seed_recipient_persona(persona)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(STAFF_PERSONAS)} staff + "
            f"{len(RECIPIENT_PERSONAS)} recipient personas (idempotent)."
        ))

    # ------------------------------------------------------------------

    def _ensure_states(self):
        """OK is the demo state for all recipient orgs; should exist via seed_demo_data."""
        State.objects.get_or_create(code="OK", defaults={"region": "Region 6"})

    def _ensure_federal_staff_group(self):
        group, _ = Group.objects.get_or_create(name=FEDERAL_STAFF_GROUP)
        return group

    def _seed_staff_persona(self, persona, staff_group):
        email, first, last, scope, role, is_super, label = persona

        u, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first,
                "last_name": last,
                "is_staff": True,
                "is_active": True,
                "is_superuser": is_super,
            },
        )
        if created:
            u.set_unusable_password()
            u.save()
        # Idempotently keep flags in sync (in case the role file was edited)
        dirty = False
        if u.first_name != first:
            u.first_name = first; dirty = True
        if u.last_name != last:
            u.last_name = last; dirty = True
        if u.is_superuser != is_super:
            u.is_superuser = is_super; dirty = True
        if not u.is_staff:
            u.is_staff = True; dirty = True
        if dirty:
            u.save()

        # Federal Staff group
        u.groups.add(staff_group)

        # Program assignments. Superuser gets none (they bypass via is_superuser).
        if is_super:
            self.stdout.write(f"  {email}  -> superuser (no program assignments needed)")
            return

        # Resolve `scope` to a Program queryset.
        if scope == "*":
            programs = Program.objects.all()
        elif isinstance(scope, str):
            programs = Program.objects.filter(office__code=scope)
        else:
            # list/tuple of program codes
            programs = Program.objects.filter(code__in=scope)

        if not programs.exists():
            self.stdout.write(self.style.WARNING(
                f"  {email}: no programs matched scope={scope} -- "
                f"did you run `migrate programs`?"
            ))
            return

        # Idempotent: only the listed programs end up assigned. If a
        # persona's scope NARROWS between seed runs (e.g. CSBG-only
        # added after starting as OCS-wide), strip stale assignments.
        target_ids = set(programs.values_list("id", flat=True))
        stale = u.program_assignments.exclude(program_id__in=target_ids)
        if stale.exists():
            stale.delete()

        for program in programs:
            UserProgramAssignment.objects.update_or_create(
                user=u, program=program,
                defaults={"role": role},
            )

        n = programs.count()
        self.stdout.write(
            f"  {email}  -> {label} ({n} program{'s' if n != 1 else ''}, role={role})"
        )

    def _seed_recipient_persona(self, persona):
        email, first, last, org_name, org_type, state_code, group_name, label = persona

        u, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first,
                "last_name": last,
                "is_staff": False,
                "is_active": True,
            },
        )
        if created:
            u.set_unusable_password()
            u.save()

        # Org
        state = State.objects.filter(code=state_code).first()
        org, _ = OrganizationProfile.objects.get_or_create(
            name=org_name,
            defaults={
                "org_type": org_type,
                "state": state,
                "contact_email": email,
            },
        )
        if org.org_type != org_type:
            org.org_type = org_type
            org.save(update_fields=["org_type"])

        # Membership + group
        group = Group.objects.filter(name=group_name).first()
        if group is None:
            self.stdout.write(self.style.WARNING(
                f"  {email}: group '{group_name}' missing -- "
                f"recipient group setup migration may not have run."
            ))
            return

        membership, _ = UserOrganizationMembership.objects.get_or_create(
            user=u, organization=org,
        )
        membership.groups.add(group)

        self.stdout.write(f"  {email}  -> {label} @ {org.name}")
