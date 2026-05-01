from django.core.exceptions import ValidationError
from django.db.models import Q

from users.permissions import (
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    RECIPIENT_AUTHORIZED_OFFICIAL,
)


def is_ao_permission_assigned(membership) -> bool:
    """Return True if any other membership in the same org already holds the AO permission,
    whether via the Recipient Authorized Official group or a direct permission assignment."""
    from organizations.models import UserOrganizationMembership

    return (
        UserOrganizationMembership.objects.filter(organization=membership.organization)
        .filter(
            Q(groups__name=RECIPIENT_AUTHORIZED_OFFICIAL)
            | Q(permissions__codename=FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL)
        )
        .exists()
    )


def enforce_single_authorized_official(sender, instance, action, pk_set, **kwargs):
    """This signal checks if the organization already has a user with the Recipient
    Authorized Official group or the individual permission to sign as authorized official.


    Raises an error if the permission is already assigned."""

    if action != "pre_add" or not pk_set:
        return

    if is_ao_permission_assigned(instance):
        _AO_ERROR = (
            f"Organization '{{org}}' already has a {RECIPIENT_AUTHORIZED_OFFICIAL}. "
            "Only one is permitted per organization."
        )
        raise ValidationError(_AO_ERROR.format(org=instance.organization))
