"""ACF program registry.

Implements STAFF-MP-01 (Program + ACFOffice) and STAFF-MP-04
(UserProgramAssignment for program-scoped staff permissions).

Architecture context: see docs/multi_program_architecture.md.

Hierarchy:
    ACFOffice (OCS, OFA, ...)
        |
        +-- Program (CSBG, TANF, Tribal_TANF, HMRF, HPOG, ...)
                |
                +-- FormDefinition.program (FK)
                |
                +-- UserProgramAssignment (user + role per program)
"""

from django.contrib.auth import get_user_model
from django.db import models

from organizations.models import BaseModel

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
