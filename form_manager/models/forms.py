from django.contrib.auth import get_user_model
from django.db import models  # type: ignore

from form_manager.constants import ALL_FORM_NAME_CHOICES, FormFamilies
from form_manager.models.fields import SemVerField
from organizations.models import BaseModel
from users.permissions import (
    FORM_EDIT,
    FORM_EDIT_DESCRIPTION,
    FORM_LIST,
    FORM_LIST_DESCRIPTION,
    FORM_START,
    FORM_START_DESCRIPTION,
    FORM_SUBMIT,
    FORM_SUBMIT_DESCRIPTION,
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL_DESCRIPTION,
    FORM_VIEW,
    FORM_VIEW_DESCRIPTION,
)

User = get_user_model()


class FormDefinition(BaseModel):
    # TODO STAFF-MP-01: add `program = ForeignKey(programs.Program)` so each
    # form is tied to a specific ACF program (CSBG, TANF, HMRF, etc.). Without
    # this, staff permissions can't be scoped per-program. See
    # docs/multi_program_architecture.md.
    # TODO STAFF-MP-03: add `cycle_type` field (annual / quarterly / monthly /
    # ad_hoc). CSBG is annual; ACF-196R is quarterly. Misclassifying surfaces
    # bad submission windows.
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

        permissions = [
            (FORM_LIST, FORM_LIST_DESCRIPTION),
            (FORM_START, FORM_START_DESCRIPTION),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.name} (v{self.variant})"


class FormEntry(BaseModel):
    # Status lifecycle:
    #   draft       -- recipient drafting (CORE recipient flow)
    #   submitted   -- recipient submitted, awaiting staff review
    #   in_progress -- recipient editing after a return (CORE-161 acknowledgements pending)
    #   returned    -- federal staff returned with review items (CORE-168, AO sig cleared per CORE-43)
    #   amended     -- federal staff edited on behalf (CORE-167), awaiting AO re-sig
    #   accepted    -- final determination = Accepted, locked (CORE-44, CORE-45)
    #   closed      -- final determination = Closed without Acceptance, locked (CORE-44, CORE-45)
    #   archived    -- end-of-life
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("in_progress", "In Progress"),
        ("returned", "Returned"),
        ("amended", "Amended"),
        ("accepted", "Accepted"),
        ("closed", "Closed without Acceptance"),
        ("archived", "Archived"),
    ]

    DETERMINATION_OUTCOMES = [
        ("accepted", "Accepted"),
        ("closed", "Closed without Acceptance"),
    ]

    form_definition = models.ForeignKey(FormDefinition, on_delete=models.PROTECT)
    organization = models.ForeignKey("organizations.OrganizationProfile", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.JSONField(default=dict)
    version_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    submitted_at = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    # Final determination (CORE-44, CORE-45). Set when staff finalizes the
    # submission. Null until then. Once set, status is 'accepted' or 'closed'
    # and locked=True. Cannot be reverted at the application layer.
    determination_outcome = models.CharField(
        max_length=20, choices=DETERMINATION_OUTCOMES, null=True, blank=True
    )
    determination_notes = models.TextField(blank=True)
    determined_at = models.DateTimeField(null=True, blank=True)
    determined_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="determined_submissions",
    )

    class Meta(BaseModel.Meta):
        unique_together = ("organization", "form_definition", "version_number")
        ordering = ["-updated_at"]
        permissions = [
            (FORM_VIEW, FORM_VIEW_DESCRIPTION),
            (FORM_EDIT, FORM_EDIT_DESCRIPTION),
            (FORM_SUBMIT, FORM_SUBMIT_DESCRIPTION),
            (
                FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
                FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL_DESCRIPTION,
            ),
            # Federal Staff permissions (CORE-132). Cross-region view per CORE-29.
            ("staff_view_any_submission",
             "Federal Staff -- view any submission regardless of region (CORE-29, CORE-132)"),
            ("staff_edit_on_behalf",
             "Federal Staff -- edit any submission on behalf of recipient (CORE-167)"),
            ("staff_return_submission",
             "Federal Staff -- return a submission with review items (CORE-168, CORE-169)"),
            ("staff_determine_submission",
             "Federal Staff -- record final determination (Accept / Close) (CORE-44, CORE-45)"),
            ("staff_archive_submission",
             "Federal Staff -- archive a submission (CORE-132)"),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.organization.name} - {self.form_definition.name} (v{self.version_number})"

    @property
    def is_resolved(self) -> bool:
        """True if a final determination has been recorded (CORE-45 lock)."""
        return self.status in ("accepted", "closed")

    @property
    def is_returned_or_in_progress(self) -> bool:
        return self.status in ("returned", "in_progress")

    @property
    def returns_used(self) -> int:
        """Number of returns issued. Used for CORE-169 one-return enforcement."""
        return self.staff_returns.count() if hasattr(self, "staff_returns") else 0


class FormAuditTrail(BaseModel):
    form_entry = models.ForeignKey(FormEntry, on_delete=models.CASCADE, related_name="audits")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Actions:
    #   create, save, submit, amend, lock, unlock, archive, unarchive (existing)
    #   edit_on_behalf, return, ao_signature_cleared,
    #   accept, close, ack_review_item (new for staff workflow)
    action = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    # Required rationale for edit_on_behalf actions (CORE-167).
    # Blank for other action types. Plain text only, immutable after save.
    rationale = models.TextField(
        blank=True,
        help_text="Required for edit_on_behalf actions per CORE-167. Immutable after save.",
    )

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

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_entry} {self.field_name} changed by {self.user}"
