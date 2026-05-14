"""
Custom Authentication Backends and OIDC Hooks for CSFEER.

This module contains:
1. EmailOIDCAuthenticationBackend: A custom OIDC backend that authenticates users based on email
   address instead of username, allowing for auto-provisioning of users via OIDC.
2. extend_user_with_roles: A hook function called after successful OIDC login to synchronize
   user roles, groups, and organization membership based on OIDC claims.
"""

from inspect import signature
from typing import TYPE_CHECKING, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from oauth2_authcodeflow.auth import AuthenticationBackend
from oauth2_authcodeflow.conf import settings

from users.models import UserProfile

if TYPE_CHECKING:
    from users.models import CoreUser


class EmailOIDCAuthenticationBackend(AuthenticationBackend):
    """
    Custom OIDC Authentication Backend that uses email as the primary identifier.

    This backend overrides the default behavior to look up or create users based on their
    email address provided in the OIDC claims, rather than the 'sub' or 'username' claim.
    """

    def get_or_create_user(self, request, id_claims, access_token) -> AbstractUser:
        """
        Retrieve or create a user based on the email claim in the ID token.

        Args:
            request: The HTTP request.
            id_claims (dict): The claims from the ID token.
            access_token (str): The access token.

        Returns:
            User: The authenticated (and potentially created) user instance.

        Raises:
            SuspiciousOperation: If the email claim is missing from the token.
        """
        claims = self.get_full_claims(request, id_claims, access_token)

        # Get email from claims
        email_claim = settings.OIDC_OP_EXPECTED_EMAIL_CLAIM
        email = claims.get(email_claim)

        if not email:
            if callable(settings.OIDC_EMAIL_CLAIM):
                email = settings.OIDC_EMAIL_CLAIM(claims)
            elif settings.OIDC_EMAIL_CLAIM:
                email = claims.get(settings.OIDC_EMAIL_CLAIM)

        if not email:
            # If we still don't have an email, we can't create/get a user
            # This might raise an error or return None depending on desired behavior
            # For now, let's raise an exception or let the parent handle it (which would fail
            # on username). But since we are overriding, we must handle it.
            from django.core.exceptions import SuspiciousOperation

            raise SuspiciousOperation("Email claim not found in OIDC token")

        CoreUser = cast("CoreUser", get_user_model())
        RecipientUser = CoreUser.get_recipient_user_model()
        # Use email for lookup instead of username
        user, created = RecipientUser.objects.get_or_create(email=email)
        user = cast(AbstractUser, user)

        self.update_user(user, created, claims, request, access_token)
        user.save()
        return user

    def update_user(
        self, user: AbstractUser, created: bool, claims: dict, request, access_token: str
    ) -> None:
        """Overloaded this method to stop clobbering the first and last name values
        that have been added to the local app's DB."""

        if not user.first_name:
            if callable(settings.OIDC_FIRSTNAME_CLAIM):
                user.first_name = str(settings.OIDC_FIRSTNAME_CLAIM(claims))
            else:
                user.first_name = claims.get(settings.OIDC_FIRSTNAME_CLAIM, "")

        if not user.last_name:
            if callable(settings.OIDC_LASTNAME_CLAIM):
                user.last_name = str(settings.OIDC_LASTNAME_CLAIM(claims))
            else:
                user.last_name = claims.get(settings.OIDC_LASTNAME_CLAIM, "")

        if settings.OIDC_UNUSABLE_PASSWORD or created:
            user.set_unusable_password()

        if callable(settings.OIDC_EXTEND_USER):
            extend_user = settings.OIDC_EXTEND_USER
            if len(signature(extend_user).parameters) > 2:
                extend_user(user, claims, request, access_token)
            else:  # backward compatibility
                extend_user(user, claims)
        user.is_active = True

    @staticmethod
    def extend_user_with_roles(user, claims, request=None, access_token=None):
        user.first_name = user.first_name or claims.get("given_name", "")
        user.last_name = user.last_name or claims.get("family_name", "")
        user.save(update_fields=["first_name", "last_name"])

        profile, _ = UserProfile.objects.get_or_create(user=user)
        phone = claims.get("phone_number", "")
        if phone:
            profile.phone_number = phone
            profile.save(update_fields=["phone_number"])
