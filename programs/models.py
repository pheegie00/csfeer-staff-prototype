"""ACF program registry + per-form lifecycle scaffolding.

Implements:
- STAFF-MP-01 (Program + ACFOffice)
- STAFF-MP-04 (UserProgramAssignment for program-scoped staff permissions)
- CORE-22    (FormScoping  -- which recipient orgs can see / fill out a form)
- CORE-25    (SubmissionWindow -- open/close dates per form per fiscal year)

Architecture context: see docs/multi_program_architecture.md.

Hierarchy:
    ACFOffice (OCS, OFA, ...)
        |
        +-- Program (CSBG, TANF, Tribal_TANF, HMRF, HPOG, ...)
                |
                +-- FormDefinition.program (FK)
                        |
                        +-- FormScoping       (1:1, CORE-22)
                        +-- SubmissionWindow  (N per FY, CORE-25)
                |
                +-- UserProgramAssignment (user + role per program)
"""

from datetime import datetime, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from organizations.models import BaseModel, OrgType

User = get_user_model()


class ACFOffice(BaseModel):
    """An ACF office (e.g., OCS, OFA, ANA, OHS).

    Each Program rolls up to one office. Used for organizational
    reporting and for permission boundaries that span programs
    within an office (e.g., an OFA-wide auditor).
    """

    code = models.CharField(
        max_length=20, unique=True,
        help_text="Short code, all-caps (OCS, OFA, ANA, etc.).",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = ["code"]
        verbose_name = "ACF Office"
        verbose_name_plural = "ACF Offices"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.code} -- {self.name}"


class Program(BaseModel):
    """A funded grant program administered by an ACF office.

    Examples: CSBG (OCS), TANF (OFA), Tribal TANF (OFA), HMRF (OFA),
    HPOG (OFA, currently inactive).

    Forms hang off programs via FormDefinition.program. Staff are
    assigned to programs via UserProgramAssignment; their permissions
    in CORE are scoped to the programs they're assigned to.
    """

    code = models.CharField(
        max_length=50, unique=True,
        help_text="Short code (CSBG, TANF, TRIBAL_TANF, HMRF, HPOG).",
    )
    name = models.CharField(max_length=200)
    office = models.ForeignKey(
        ACFOffice, on_delete=models.PROTECT, related_name="programs",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="False for programs in dormant funding cycles (e.g., HPOG today).",
    )

    class Meta(BaseModel.Meta):
        ordering = ["office__code", "code"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.code} ({self.office.code})"


class UserProgramAssignment(BaseModel):
    """Maps a Federal Staff user to the programs they cover.

    STAFF-MP-04: scopes "who sees what" beyond the binary Federal
    Staff group from CORE-132. A user in the Federal Staff group
    sees only submissions whose form's program is in their
    assigned programs.

    Roles per program:
        reviewer   -- can view + edit on behalf + return + determine
        auditor    -- read-only + can run reports / exports
        admin      -- above + Form Builder access for this program

    Future: per-program role -> Django permissions mapping.
    """

    ROLE_CHOICES = [
        ("reviewer", "Reviewer"),
        ("auditor", "Auditor"),
        ("admin", "Program Admin"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="program_assignments",
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="user_assignments",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="reviewer")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        unique_together = ("user", "program")
        ordering = ["user__email", "program__code"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user.email} -> {self.program.code} ({self.role})"


# ============================================================
# SUBMISSION WINDOW (CORE-25)
# ============================================================

class SubmissionWindowStatus:
    UPCOMING = "upcoming"
    OPEN = "open"
    PAST_DUE = "past_due"

    CHOICES = [
        (UPCOMING, "Upcoming"),
        (OPEN, "Open"),
        (PAST_DUE, "Past Due"),
    ]


class SubmissionWindow(BaseModel):
    """Open/close dates for a form template, per fiscal year (CORE-25).

    Stored:
      form_definition  -- FK
      fiscal_year      -- string e.g. "FY26"
      opens_at         -- datetime: BEFORE this, recipients cannot
                          create new drafts (status = Upcoming)
      closes_at        -- datetime: AFTER this, no NEW drafts can be
                          started, but existing drafts can still be
                          edited + submitted. Status = Past Due.

    Unique on (form_definition, fiscal_year): one window per form
    per FY. Multiple FYs per form = multiple rows.

    Status is derived (not stored): see status_at() / status property.
    """

    form_definition = models.ForeignKey(
        "form_manager.FormDefinition",
        on_delete=models.CASCADE,
        related_name="submission_windows",
    )
    fiscal_year = models.CharField(
        max_length=10,
        help_text="e.g., 'FY26', 'FY26-Q1'. Format is program-conventional.",
    )
    opens_at = models.DateTimeField(
        help_text="When recipients can start new drafts. Before this -> Upcoming.",
    )
    closes_at = models.DateTimeField(
        help_text="After this, no new drafts. Existing drafts may still be "
                  "edited + submitted per CORE-25.",
    )

    class Meta(BaseModel.Meta):
        unique_together = ("form_definition", "fiscal_year")
        ordering = ["form_definition", "-opens_at"]
        indexes = [
            models.Index(fields=["form_definition", "fiscal_year"]),
            models.Index(fields=["opens_at"]),
            models.Index(fields=["closes_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.form_definition} -- {self.fiscal_year}"

    # ---- Status derivation ----

    def status_at(self, when=None):
        """Return SubmissionWindowStatus for the given moment (defaults to now)."""
        now = when or timezone.now()
        if now < self.opens_at:
            return SubmissionWindowStatus.UPCOMING
        if now > self.closes_at:
            return SubmissionWindowStatus.PAST_DUE
        return SubmissionWindowStatus.OPEN

    @property
    def status(self):
        return self.status_at()

    @property
    def is_open(self):
        return self.status == SubmissionWindowStatus.OPEN

    @property
    def is_upcoming(self):
        return self.status == SubmissionWindowStatus.UPCOMING

    @property
    def is_past_due(self):
        return self.status == SubmissionWindowStatus.PAST_DUE

    @property
    def days_until_open(self):
        """Days until opens_at (only meaningful when Upcoming). Negative if already open."""
        delta = self.opens_at - timezone.now()
        return delta.days

    @property
    def days_until_close(self):
        """Days until closes_at (only meaningful when Open). Negative if Past Due."""
        delta = self.closes_at - timezone.now()
        return delta.days


# ============================================================
# FORM SCOPING (CORE-22)
# ============================================================

class FormScoping(BaseModel):
    """Which recipient orgs can see / fill out a given FormDefinition.

    Two scoping mechanisms, additive:

    1. RULE-BASED -- scope_to_org_types is a list of OrgType values.
       Any OrganizationProfile whose org_type is in this list is
       in scope. Lets CSBG say "all 574 Federally Recognized Tribes"
       without listing them individually.

    2. EXPLICIT -- explicit_orgs is an M2M of OrganizationProfile.
       Orgs in this set are in scope EVEN IF their org_type is not
       in scope_to_org_types. Useful for one-off exceptions.

    The is_org_in_scope() helper unions both.
    """

    form_definition = models.OneToOneField(
        "form_manager.FormDefinition",
        on_delete=models.CASCADE,
        related_name="scoping",
    )
    scope_to_org_types = models.JSONField(
        default=list, blank=True,
        help_text="List of OrgType values: forms apply to all orgs of these types. "
                  "Empty list = no rule (only explicit_orgs apply).",
    )
    explicit_orgs = models.ManyToManyField(
        "organizations.OrganizationProfile",
        blank=True,
        related_name="scoped_forms",
        help_text="Additional specific orgs in scope, regardless of org_type rule.",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Form scoping"
        verbose_name_plural = "Form scopings"

    def __str__(self) -> str:  # pragma: no cover
        return f"Scoping for {self.form_definition}"

    # ---- Validation ----

    def clean(self):
        """Ensure scope_to_org_types contains only valid OrgType values."""
        from django.core.exceptions import ValidationError
        valid_types = {c[0] for c in OrgType.choices}
        bad = set(self.scope_to_org_types or []) - valid_types
        if bad:
            raise ValidationError(
                f"Unknown org_type(s) in scope_to_org_types: {sorted(bad)}. "
                f"Valid: {sorted(valid_types)}"
            )

    # ---- Membership check ----

    def is_org_in_scope(self, org) -> bool:
        """Returns True if `org` (OrganizationProfile) is in scope.

        Rule + explicit are additive (union).
        """
        if org is None:
            return False
        if org.org_type in (self.scope_to_org_types or []):
            return True
        # explicit_orgs is M2M -- avoid extra query if rule already passed
        return self.explicit_orgs.filter(pk=org.pk).exists()

    def in_scope_org_count(self) -> int:
        """Compute the total number of orgs currently in scope.

        Useful for the Form Builder UI to show "574 of 574 Tribes" etc.
        Combines rule-based + explicit, deduplicated.
        """
        from organizations.models import OrganizationProfile
        qs = OrganizationProfile.objects.none()
        if self.scope_to_org_types:
            qs = qs | OrganizationProfile.objects.filter(org_type__in=self.scope_to_org_types)
        qs = qs | self.explicit_orgs.all()
        return qs.distinct().count()
