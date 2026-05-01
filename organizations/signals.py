from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from organizations.utils import is_ao_permission_assigned
from users.permissions import (
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    RECIPIENT_AUTHORIZED_OFFICIAL,
)


def enforce_single_authorized_official(sender, instance, action, pk_set, **kwargs):
    if action != "pre_add" or not pk_set:
        return

    from organizations.models import UserOrganizationMembership

    if (
        sender == UserOrganizationMembership.groups.through
        and not Group.objects.filter(pk__in=pk_set, name=RECIPIENT_AUTHORIZED_OFFICIAL).exists()
    ):
        return

    if (
        sender == UserOrganizationMembership.permissions.through
        and not Permission.objects.filter(
            pk__in=pk_set, codename=FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL
        ).exists()
    ):
        return

    if is_ao_permission_assigned(instance.organization):
        raise ValidationError(
            f"Organization '{instance.organization}' already has a "
            f"{RECIPIENT_AUTHORIZED_OFFICIAL}. Only one is permitted per organization."
        )
