"""Audit-only models for staff_review.

Separate file from staff_review.models so the schema-evolution of
audit tables stays clean and reviewable.

CORE-21 -- account change audit (user create / org / role / deactivate)
CORE-35 -- operational form activity log (covered by FormAuditTrail,
            this file extends with login/logout events)
CORE-36 -- compliance-grade audit log (FormAuditTrail + this file)
CORE-47 -- system-wide tamper-evident infrastructure log (FISMA / NIST
            800-53). This file's `SystemEvent` is the staff_review
            slice of that broader requirement.

All audit rows are immutable at the application layer: save() on an
existing row raises AuditTrailImmutableError; delete() always raises.
DB-level immutability (revoking UPDATE/DELETE grants on the audit
tables) is the production-deploy concern, tracked in CORE-47.
"""

from django.contrib.auth import get_user_model
from django.db import models

from organizations.models import BaseModel

User = get_user_model()


class AuditTrailImmutableError(Exception):
    """Raised when something tries to mutate or delete an audit row."""


class ImmutableAuditMixin:
    """Block updates + deletes once a row exists.

    Inherit from this BEFORE BaseModel in the class definition so the
    mixin's save() / delete() overrides take precedence in MRO.
    """

    def save(self, *args, **kwargs):
        # _state.adding is True only for the very first save of an instance.
        # UUIDField primary keys are set BEFORE save, so checking pk doesn't work.
        if not self._state.adding:
            raise AuditTrailImmutableError(
                f"{self.__class__.__name__}({self.pk}) is immutable -- "
                "audit rows cannot be edited after save (CORE-36, CORE-47)."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise AuditTrailImmutableError(
            f"{self.__class__.__name__}({self.pk}) cannot be deleted -- audit log is append-only (CORE-36, CORE-47)."
        )


class AccountAuditTrail(ImmutableAuditMixin, BaseModel):
    """Account-level audit events (CORE-21).

    Covers: user created, deactivated, reactivated, role/group added or
    removed, organization membership added or removed.

    Distinct from FormAuditTrail (form-level actions) and SystemEvent
    (login/logout). Account changes don't always have a form context.
    """

    ACTIONS = [
        ("user_created", "User created"),
        ("user_deactivated", "User deactivated"),
        ("user_reactivated", "User reactivated"),
        ("group_added", "Group / role added"),
        ("group_removed", "Group / role removed"),
        ("org_membership_added", "Organization membership added"),
        ("org_membership_removed", "Organization membership removed"),
        ("permission_added", "Permission granted"),
        ("permission_removed", "Permission revoked"),
    ]

    # Who is the change about (target).
    target_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="account_audit_events",
        help_text="The user whose account changed.",
    )
    # Who made the change. NULL if system-initiated.
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="account_audit_actions",
        help_text="The user who initiated the change. NULL = system / migration.",
    )
    action = models.CharField(max_length=40, choices=ACTIONS)
    # Optional context: which org, which group, which permission, etc.
    context = models.JSONField(
        default=dict, blank=True,
        help_text="Free-form context per action: e.g., {'group':'Federal Staff'} or {'org_id':'<uuid>'}.",
    )
    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target_user", "-created_at"]),
            models.Index(fields=["actor", "-created_at"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.action} on {self.target_user_id} by {self.actor_id or 'system'} @ {self.created_at}"


class SystemEvent(ImmutableAuditMixin, BaseModel):
    """System-level event log for CORE-36 / CORE-47.

    Covers events that don't fit FormAuditTrail (form-scoped) or
    AccountAuditTrail (account-scoped): logins, logouts, CSV exports,
    bulk operations.
    """

    KIND_CHOICES = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("login_failed", "Login failed"),
        ("export_csv", "CSV export downloaded"),
        ("audit_log_viewed", "Audit log viewed"),
    ]

    kind = models.CharField(max_length=40, choices=KIND_CHOICES)
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="system_events",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    # Free-form structured detail per event type
    detail = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["kind", "-created_at"]),
            models.Index(fields=["actor", "-created_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.kind} by {self.actor_id or 'anon'} @ {self.created_at}"
