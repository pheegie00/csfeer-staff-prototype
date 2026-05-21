from typing import cast

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from localflavor.us.models import USStateField

from core.models import BaseActivityFields, BaseModel
from organizations.constants import RegionChoices


class OrgType(models.TextChoices):
    """Recipient organization type (STAFF-MP-02).

    Different ACF programs serve different mixes of recipient orgs:
        CSBG: TRIBE only (currently)
        TANF: STATE + TERRITORY
        HMRF: CBO + FAITH_BASED + TRIBE + WORKFORCE + HIGHER_ED
        HPOG: HIGHER_ED + WORKFORCE + TRIBE + STATE + CBO
    """
    TRIBE       = "tribe", "Federally Recognized Tribe"
    TRIBAL_ORG  = "tribal_org", "Tribal Organization"
    STATE       = "state", "State Government"
    TERRITORY   = "territory", "U.S. Territory"
    HIGHER_ED   = "higher_ed", "Higher Education Institution"
    WORKFORCE   = "workforce_agency", "Workforce System Agency"
    CBO         = "cbo", "Community-Based Organization"
    FAITH_BASED = "faith_based", "Faith-Based Organization"
    OTHER       = "other", "Other"


class OrganizationProfile(BaseModel):
    """Recipient organization.

    Per STAFF-MP-02, org_type identifies the recipient flavor. Today all
    existing rows backfill to TRIBE (CSBG-only history); future TANF/HMRF
    seeding adds STATE, CBO, etc.
    """

    name = models.CharField(max_length=255)
    org_type = models.CharField(
        max_length=30, choices=OrgType.choices, default=OrgType.TRIBE,
        help_text="STAFF-MP-02: Tribal / State / Territory / CBO / Higher Ed / etc.",
    )
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    state = models.ForeignKey("State", on_delete=models.PROTECT, related_name="organizations")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class UserOrganizationMembership(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="org_memberships"
    )
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="org_memberships",
        help_text="The permission group that the user belongs to for this organization",
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="org_memberships",
        help_text=(
            "Specific permissions individually assigned to this user "
            "for this organization in addition to those assiged by any "
            "permission groups"
        ),
    )

    class Meta(BaseModel.Meta):
        unique_together = ("user", "organization")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user} → {self.organization}"


class State(BaseActivityFields):
    """Represents a US state and its designated ACF region."""

    code = USStateField(unique=True, primary_key=True)
    region = models.CharField(choices=RegionChoices)

    class Meta(BaseActivityFields.Meta):
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["region", "code"]),
        ]

    def __str__(self) -> str:
        return cast(str, self.code)
