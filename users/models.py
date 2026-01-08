from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from users.managers import CoreUserManager


class CoreUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: CoreUserManager = CoreUserManager()  # type: ignore[assignment]

    def __str__(self):
        return self.email


class UserProfile(BaseModel):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="profile")
    oidc_user_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique identifier from OIDC provider (Login.gov or Keycloak)",
    )

    def __str__(self):
        return f"Profile for {self.user}"
