"""
Custom Authentication Backends and OIDC Hooks for CSFEER.

This module contains:
1. EmailOIDCAuthenticationBackend: A custom OIDC backend that authenticates users based on email
   address instead of username, allowing for auto-provisioning of users via OIDC.
2. extend_user_with_roles: A hook function called after successful OIDC login to synchronize
   user roles, groups, and organization membership based on OIDC claims.
"""

from typing import cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from oauth2_authcodeflow.auth import AuthenticationBackend
from oauth2_authcodeflow.conf import settings

from form_manager.models import OrganizationProfile, UserOrganizationMembership
from users.models import UserProfile


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

        User = get_user_model()
        # Use email for lookup instead of username
        user, created = User.objects.get_or_create(email=email)
        user = cast(AbstractUser, user)

        self.update_user(user, created, claims, request, access_token)
        user.save()
        return user


def extend_user_with_roles(user, claims, request=None, access_token=None):
    """
    Called automatically on each login to extend user properties with OIDC claims.

    Args:
        user: Django user instance
        claims: ID token claims from OIDC provider
        request: HTTP request object (optional)
        access_token: Access token string (optional)
    """
    # Extract roles from Keycloak standard realm_access claim
    roles = claims.get("realm_access", {}).get("roles", [])

    # Clear existing groups and assign based on OIDC roles
    user.groups.clear()

    for role_name in roles:
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)

    # Assign staff/superuser based on specific roles
    user.is_staff = "csfeer_admin" in roles or "csfeer_staff" in roles
    user.is_superuser = "superuser" in roles or "csfeer_admin" in roles
    user.save()

    # Update Profile with OIDC ID (sub claim)
    if not hasattr(user, "profile"):
        UserProfile.objects.create(user=user)

    user.profile.oidc_user_id = claims.get("sub")
    user.profile.save()

    # Ensure user has an organization
    if not UserOrganizationMembership.objects.filter(user=user).exists():
        # Create a personal organization for the user
        org_name = f"{user.email}'s Organization"
        org = OrganizationProfile.objects.create(name=org_name, contact_email=user.email)
        UserOrganizationMembership.objects.create(user=user, organization=org, role="admin")
