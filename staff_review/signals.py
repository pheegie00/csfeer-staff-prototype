"""Audit signal handlers (CORE-21, CORE-36).

Auto-write audit rows on:
- user_logged_in / user_logged_out / user_login_failed  -> SystemEvent
- User.is_active flip                                  -> AccountAuditTrail
- Group membership add/remove                          -> AccountAuditTrail
- Permission grant/revoke                              -> AccountAuditTrail
- UserOrganizationMembership add/remove                -> AccountAuditTrail

Signal receivers live in their own module so the import side-effect
(`from staff_review import signals`) is wired exactly once via
StaffReviewConfig.ready().
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed,
)
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from staff_review.audit_models import AccountAuditTrail, SystemEvent

User = get_user_model()


def _ip(request):
    if not request:
        return None
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _ua(request):
    return (request.META.get("HTTP_USER_AGENT", "") if request else "")[:512]


# ============================================================
# SystemEvent -- login / logout (CORE-36)
# ============================================================

@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    SystemEvent.objects.create(
        kind="login", actor=user,
        ip_address=_ip(request), user_agent=_ua(request),
        notes=f"{user.email} signed in",
    )


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if user is None:
        return
    SystemEvent.objects.create(
        kind="logout", actor=user,
        ip_address=_ip(request), user_agent=_ua(request),
        notes=f"{user.email} signed out",
    )


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request=None, **kwargs):
    # credentials may include email/username -- log without password
    safe = {k: v for k, v in (credentials or {}).items() if k not in ("password",)}
    SystemEvent.objects.create(
        kind="login_failed", actor=None,
        ip_address=_ip(request), user_agent=_ua(request),
        detail=safe,
        notes=f"Login attempt failed for {safe.get('username') or safe.get('email') or '(unknown)'}",
    )


# ============================================================
# AccountAuditTrail -- user activation flips (CORE-21)
# ============================================================
# Cache prior is_active state so we know if it changed on this save.

_prior_active = {}


@receiver(post_save, sender=User)
def on_user_save(sender, instance, created, **kwargs):
    if created:
        AccountAuditTrail.objects.create(
            target_user=instance, actor=None,
            action="user_created",
            context={"email": instance.email},
            notes="User created (signal-detected; actor unknown unless wired by caller)",
        )
        _prior_active[instance.pk] = instance.is_active
        return

    was_active = _prior_active.get(instance.pk)
    if was_active is not None and was_active != instance.is_active:
        AccountAuditTrail.objects.create(
            target_user=instance, actor=None,
            action="user_reactivated" if instance.is_active else "user_deactivated",
            context={"is_active": instance.is_active},
        )
    _prior_active[instance.pk] = instance.is_active


# ============================================================
# AccountAuditTrail -- group membership changes (CORE-21)
# ============================================================

@receiver(m2m_changed, sender=User.groups.through)
def on_user_groups_changed(sender, instance, action, pk_set, **kwargs):
    if action not in ("post_add", "post_remove"):
        return
    if not pk_set:
        return
    audit_action = "group_added" if action == "post_add" else "group_removed"
    for group_pk in pk_set:
        try:
            group_name = Group.objects.get(pk=group_pk).name
        except Group.DoesNotExist:
            group_name = f"(deleted group {group_pk})"
        AccountAuditTrail.objects.create(
            target_user=instance, actor=None,
            action=audit_action,
            context={"group": group_name, "group_id": group_pk},
        )


# ============================================================
# AccountAuditTrail -- explicit permission grants (CORE-21)
# ============================================================

@receiver(m2m_changed, sender=User.user_permissions.through)
def on_user_perms_changed(sender, instance, action, pk_set, **kwargs):
    if action not in ("post_add", "post_remove"):
        return
    if not pk_set:
        return
    audit_action = "permission_added" if action == "post_add" else "permission_removed"
    for perm_pk in pk_set:
        try:
            perm = Permission.objects.get(pk=perm_pk)
            perm_label = f"{perm.content_type.app_label}.{perm.codename}"
        except Permission.DoesNotExist:
            perm_label = f"(deleted perm {perm_pk})"
        AccountAuditTrail.objects.create(
            target_user=instance, actor=None,
            action=audit_action,
            context={"permission": perm_label, "permission_id": perm_pk},
        )


# ============================================================
# AccountAuditTrail -- org membership add/remove (CORE-21)
# ============================================================

@receiver(post_save, sender="organizations.UserOrganizationMembership")
def on_org_membership_added(sender, instance, created, **kwargs):
    if not created:
        return
    AccountAuditTrail.objects.create(
        target_user=instance.user, actor=None,
        action="org_membership_added",
        context={"org_id": str(instance.organization_id), "org_name": instance.organization.name},
    )


@receiver(post_delete, sender="organizations.UserOrganizationMembership")
def on_org_membership_removed(sender, instance, **kwargs):
    AccountAuditTrail.objects.create(
        target_user=instance.user, actor=None,
        action="org_membership_removed",
        context={"org_id": str(instance.organization_id)},
    )
