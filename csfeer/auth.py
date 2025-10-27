"""
Custom user extension for OIDC authentication.
"""

from django.contrib.auth.models import Group


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
