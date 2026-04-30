from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models

from core.models import BaseModel


# Create your models here.
class OrganizationProfile(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)

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
