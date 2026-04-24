from django.conf import settings
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
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("editor", "Editor"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="editor")

    class Meta(BaseModel.Meta):
        unique_together = ("user", "organization")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user} → {self.organization} ({self.role})"
