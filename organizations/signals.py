from django.core.exceptions import ValidationError

from organizations.utils import is_ao_permission_assigned
from users.permissions import (
    RECIPIENT_AUTHORIZED_OFFICIAL,
)


def enforce_single_authorized_official(sender, instance, action, pk_set, **kwargs):
    """This signal checks if the organization already has a user with the Recipient
    Authorized Official group or the individual permission to sign as authorized official.


    Raises an error if the permission is already assigned."""

    if action != "pre_add" or not pk_set:
        return

    if is_ao_permission_assigned(instance.organization):
        AO_ERROR = (
            f"Organization '{{org}}' already has a {RECIPIENT_AUTHORIZED_OFFICIAL}. "
            "Only one is permitted per organization."
        )
        raise ValidationError(AO_ERROR.format(org=instance.organization))
