from django.core.exceptions import ValidationError
from django.db.models import Q

from users.permissions import ORG_PERMISSION_GROUPS

RECIPIENT_AUTHORIZED_OFFICIAL = next(
    name for name in ORG_PERMISSION_GROUPS if "Authorized Official" in name
)
AO_PERMISSION_CODENAME = "form_tribal_plan_can_sign_authorized_official"

_AO_ERROR = (
    f"Organization '{{org}}' already has a {RECIPIENT_AUTHORIZED_OFFICIAL}. "
    "Only one is permitted per organization."
)


def _ao_held_elsewhere(membership) -> bool:
    """Return True if any other membership in the same org already holds the AO permission,
    whether via the Recipient Authorized Official group or a direct permission assignment."""
    from organizations.models import UserOrganizationMembership

    return (
        UserOrganizationMembership.objects.filter(organization=membership.organization)
        .exclude(pk=membership.pk)
        .filter(
            Q(groups__name=RECIPIENT_AUTHORIZED_OFFICIAL)
            | Q(permissions__codename=AO_PERMISSION_CODENAME)
        )
        .exists()
    )


def enforce_single_authorized_official(sender, instance, action, pk_set, **kwargs):
    """Block adding the AO group to a membership when the org already has an AO."""
    if action != "pre_add" or not pk_set:
        return

    from django.contrib.auth.models import Group

    ao_group = Group.objects.filter(name=RECIPIENT_AUTHORIZED_OFFICIAL).first()
    if ao_group is None or ao_group.pk not in pk_set:
        return

    if _ao_held_elsewhere(instance):
        raise ValidationError(_AO_ERROR.format(org=instance.organization))


def enforce_single_ao_direct_permission(sender, instance, action, pk_set, **kwargs):
    """Block directly assigning the AO permission to a membership when the org already has an AO."""
    if action != "pre_add" or not pk_set:
        return

    from django.contrib.auth.models import Permission

    ao_perm = Permission.objects.filter(codename=AO_PERMISSION_CODENAME).first()
    if ao_perm is None or ao_perm.pk not in pk_set:
        return

    if _ao_held_elsewhere(instance):
        raise ValidationError(_AO_ERROR.format(org=instance.organization))
