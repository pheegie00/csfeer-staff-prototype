"""Staff workflow models.

Sits alongside the existing form_manager.FormEntry / FormAuditTrail
infrastructure. Models here are scoped to the federal-staff side:

- FormReturn         -- one record per "return for revision" action
                        on a submission (CORE-168). One return per
                        FormEntry max for the lifetime of the
                        submission (CORE-169 enforced in business
                        logic, not at the DB level so we can audit
                        attempts).
- FormReturnItem     -- the discrete review items attached to a
                        return (CORE-168 acceptance criteria
                        "one or more items"). Each item is independently
                        acknowledged by the recipient before resubmit
                        (CORE-161).

Determination is modeled as fields on FormEntry itself (1:1).
Edit-on-behalf rationale is modeled as the new rationale field on
FormAuditTrail (1 trail entry per save session, multiple FormAuditDetail
field-change rows under it).

Phase 4 (out of scope for this commit): SubmissionEvent for the
combined activity feed shown in the rail. Currently derived on the
fly from FormAuditTrail + FormReturn + AO sign events.
"""

from django.contrib.auth import get_user_model
from django.db import models

from form_manager.models.forms import FormEntry
from organizations.models import BaseModel

User = get_user_model()


class FormReturn(BaseModel):
    """A single Federal-Staff-initiated return of a submission.

    Per CORE-169, at most one return is allowed per submission lifetime.
    Enforce at the view/service layer; allow the schema to record
    multiple historically if needed for audit purposes.
    """

    form_entry = models.ForeignKey(
        FormEntry, on_delete=models.CASCADE, related_name="staff_returns"
    )
    returned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="returns_issued"
    )
    returned_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(
        blank=True,
        help_text="Optional summary note that opens the recipient notification email (CORE-42).",
    )

    # Flag set when the AO signature was cleared as part of the return
    # (CORE-43). Almost always True for tribal_plan submissions; False
    # for forms that don't require AO sig (annual-report-short).
    #
    # TODO STAFF-MP-01: 'AO signature' is a Tribal Plan concept. Non-CSBG
    # programs (TANF financial reports, HMRF performance measures) have
    # different signatory roles (preparer / certifier in TANF). Generalize
    # this field into a `signatures_cleared` JSONField or polymorphic state
    # when adding the first non-CSBG program. See
    # docs/multi_program_architecture.md.
    ao_signature_cleared = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = ["-returned_at"]
        permissions = [
            ("view_any_return", "View any submission return record"),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Return of {self.form_entry} by {self.returned_by} at {self.returned_at}"

    @property
    def items_count(self) -> int:
        return self.items.count()

    @property
    def ack_count(self) -> int:
        return self.items.filter(acknowledged_at__isnull=False).count()

    @property
    def fully_acknowledged(self) -> bool:
        """True when every item has been acked. Recipient cannot resubmit until then (CORE-161)."""
        total = self.items_count
        return total > 0 and self.ack_count == total


class FormReturnItem(BaseModel):
    """One discrete review item attached to a return.

    Recipient acknowledges each item before resubmit (CORE-161).
    Functional parity with the existing paper review memo (CORE-79 design analysis).
    """

    form_return = models.ForeignKey(
        FormReturn, on_delete=models.CASCADE, related_name="items"
    )
    # Free-text location pointers. Could be tightened to FK against form
    # schema sections in a future iteration; for now matches the prototype's
    # 'section + optional field' shape.
    section = models.CharField(max_length=200, blank=True)
    field = models.CharField(max_length=200, blank=True)
    text = models.TextField(help_text="The review-item description shown to the recipient.")

    order = models.PositiveSmallIntegerField(default=1, help_text="Display order within the return.")

    # Acknowledgement (CORE-161). Set by recipient when they address the item.
    acknowledged_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="return_items_acknowledged",
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledgement_response = models.TextField(
        blank=True,
        help_text="Recipient's reply text shown to staff when reviewing the resubmission.",
    )

    class Meta(BaseModel.Meta):
        ordering = ["form_return", "order"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Item {self.order} on {self.form_return}: {self.text[:50]}"

    @property
    def is_acknowledged(self) -> bool:
        return self.acknowledged_at is not None
