from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class OrganizationProfile(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class UserOrganizationMembership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("editor", "Editor"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="editor")

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user} → {self.organization} ({self.role})"


class FormDefinition(models.Model):
    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="A unique identifier for this form definition, like an OMB form number.",
    )
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=10, default="1.0")
    description = models.TextField(blank=True, null=True)
    schema = models.JSONField(default=dict)
    schema_class = models.CharField(
        max_length=255,
        help_text="The name of the pydantic form schema class",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("code", "version")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.title} (v{self.version})"


class FormEntry(models.Model):
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
    updated_at = models.DateTimeField(auto_now=True)
    locked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "form_definition", "version_number")
        ordering = ["-updated_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.organization.name} - {self.form_definition.title} (v{self.version_number})"


class FormAuditTrail(models.Model):
    form_entry = models.ForeignKey(FormEntry, on_delete=models.CASCADE, related_name="audits")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(
        max_length=50
    )  # create, save, submit, amend, lock, unlock, archive, unarchive
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_entry} - {self.action} by {self.user}"


class FormAuditDetail(models.Model):
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
