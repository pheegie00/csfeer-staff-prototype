"""
Form permission authentication backend

This backend doesn't actually authentication anyone. Instead, it just provides
standard methods on the user object to check if a user has permission.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from oauth2_authcodeflow.auth import AuthenticationBackend

if TYPE_CHECKING:
    pass


class FormPermissionBackend(AuthenticationBackend):
    """Provide an interface for checking user permissions on specific form objects."""

    def authenticate(self, request, *args, **kwargs):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        from organizations.models import OrganizationProfile, UserOrganizationMembership

        if not user_obj.is_active:  # type: ignore
            return False
        if not isinstance(obj, OrganizationProfile):
            return False  # Only handles org-scoped checks
        if user_obj.is_superuser:  # type: ignore
            return True  # ModelBackend won't fire for obj != None, so handle here

        try:
            membership = UserOrganizationMembership.objects.get(user=user_obj, organization=obj)
        except UserOrganizationMembership.DoesNotExist:
            return False

        codename = perm.split(".")[-1]

        # Direct ad-hoc permission
        if membership.permissions.filter(codename=codename).exists():
            return True

        # Group-based permission
        return membership.groups.filter(permissions__codename=codename).exists()
