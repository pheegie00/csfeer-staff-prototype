from typing import cast

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from localflavor.us.models import USStateField

from core.models import BaseActivityFields, BaseModel
from organizations.constants import RegionChoices


class OrganizationProfile(BaseModel):
    """Recipient organization (Tribe today; State / Territory / CBO / etc. when
    multi-program scaling lands).

    TODO STAFF-MP-02: add `org_type` choices field. Today every org is
    implicitly treated as a Tribe (per CSBG-only scope), but TANF will
    introduce State + Territory, HMRF will introduce CBO / Faith-Based /
    Higher Ed. See docs/multi_program_architecture.md.
    """

    name = models.CharField(max_length=255)
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
