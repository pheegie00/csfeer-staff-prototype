from django.db.models import Q

from users.permissions import (
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    RECIPIENT_AUTHORIZED_OFFICIAL,
)


def is_ao_permission_assigned(organization, exclude_pk=None) -> bool:
    """Return True if any other membership in the same org already holds the AO permission,
    whether via the Recipient Authorized Official group or a direct permission assignment."""
    from organizations.models import UserOrganizationMembership

    qs = UserOrganizationMembership.objects.filter(organization=organization).filter(
        Q(groups__name=RECIPIENT_AUTHORIZED_OFFICIAL)
        | Q(permissions__codename=FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL)
    )

    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    return qs.exists()
