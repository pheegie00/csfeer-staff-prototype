from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from typedmodels.models import TypedModel

from core.models import BaseModel
from users.managers import CoreUserManager


class CoreUser(BaseModel, AbstractUser, TypedModel):

    class Meta(BaseModel.Meta, AbstractUser.Meta, TypedModel.Meta):
        pass

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: CoreUserManager = CoreUserManager()  # type: ignore[assignment]

    @staticmethod
    def get_recipient_user_model() -> "type[RecipientUser]":
        return RecipientUser

    @staticmethod
    def get_federal_staff_user_model() -> "type[FederalStaffUser]":
        return FederalStaffUser

    def __str__(self):
        return self.email


class RecipientUser(CoreUser):

    class Meta(CoreUser.Meta):
        verbose_name = "Recipient"
        verbose_name_plural = "Recipients"


class FederalStaffUser(CoreUser):

    class Meta(CoreUser.Meta):
        verbose_name = "Federal Staff"
        verbose_name_plural = "Federal Staffers"


class UserProfile(BaseModel):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="profile")
    oidc_user_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique identifier from OIDC provider (Login.gov or Keycloak)",
    )
    phone_number = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"Profile for {self.user}"
