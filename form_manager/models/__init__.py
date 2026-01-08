from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel
from form_manager.constants import ALL_FORM_NAME_CHOICES, FormFamilies
from form_manager.models.fields import SemVerField

User = get_user_model()


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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="editor")

    class Meta(BaseModel.Meta):
        unique_together = ("user", "organization")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user} → {self.organization} ({self.role})"


class FormDefinition(BaseModel):
    family = models.CharField(
        null=False,
        blank=False,
        choices=FormFamilies.choices,
        help_text="The name of the form family",
    )
    name = models.CharField(
        max_length=255, help_text="The official name of the form.", choices=ALL_FORM_NAME_CHOICES
    )
    variant = SemVerField(
        max_length=20, default="1.0.0", help_text="The internal variant number of a form definition"
    )
    description = models.TextField(blank=True, null=True)
    schema = models.JSONField(default=dict)
    schema_class = models.CharField(
        max_length=255,
        help_text="The name of the pydantic form schema class",
    )
    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        unique_together = ("name", "variant")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.name} (v{self.variant})"


class FormEntry(BaseModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("amended", "Amended"),
        ("archived", "Archived"),
    ]

    form_definition = models.ForeignKey(FormDefinition, on_delete=models.PROTECT)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.JSONField(default=dict)
    version_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    submitted_at = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        unique_together = ("organization", "form_definition", "version_number")
        ordering = ["-updated_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.organization.name} - {self.form_definition.name} (v{self.version_number})"


class FormAuditTrail(BaseModel):
    form_entry = models.ForeignKey(FormEntry, on_delete=models.CASCADE, related_name="audits")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(
        max_length=50
    )  # create, save, submit, amend, lock, unlock, archive, unarchive
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_entry} - {self.action} by {self.user}"


class FormAuditDetail(BaseModel):
    form_entry = models.ForeignKey(
        FormEntry, on_delete=models.CASCADE, related_name="audit_details"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField(max_length=200)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_entry} {self.field_name} changed by {self.user}"
