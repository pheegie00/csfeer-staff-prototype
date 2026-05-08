from django import forms  # type: ignore
from django.contrib import admin  # type: ignore
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from organizations.models import OrganizationProfile, UserOrganizationMembership
from organizations.utils import is_ao_permission_assigned
from users.permissions import (
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    RECIPIENT_AUTHORIZED_OFFICIAL,
)


class UserOrganizationMembershipForm(forms.ModelForm):
    """Ensures only one Recipient Authorized Official can be added to an organization."""

    class Meta:
        model = UserOrganizationMembership
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        self.verify_ao_permissions(cleaned_data)
        return cleaned_data

    def verify_ao_permissions(self, cleaned_data):
        """Raises an error if we're trying to add an AO permission
        to the org when a user already has the AO permissions"""

        organization = cleaned_data.get("organization")
        if not organization:
            return cleaned_data

        exclude_pk = self.instance.pk if self.instance.pk else None
        error_msg = (
            f"Organization '{organization}' already has a {RECIPIENT_AUTHORIZED_OFFICIAL}. "
            "Only one is permitted per organization."
        )

        groups = cleaned_data.get("groups")
        if groups:
            ao_group = Group.objects.filter(name=RECIPIENT_AUTHORIZED_OFFICIAL).first()
            if (
                ao_group
                and ao_group in groups
                and is_ao_permission_assigned(organization, exclude_pk)
            ):
                raise ValidationError(error_msg)

        permissions = cleaned_data.get("permissions")
        if permissions:
            ao_perm = Permission.objects.filter(
                codename=FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL
            ).first()
            if (
                ao_perm
                and ao_perm in permissions
                and is_ao_permission_assigned(organization, exclude_pk)
            ):
                raise ValidationError(error_msg)


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "state",
        "state__region",
        "contact_email",
        "contact_phone",
        "created_at",
    )
    search_fields = ("name", "contact_email", "state", "state__region")


@admin.register(UserOrganizationMembership)
class UserOrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "user__email", "organization")
    search_fields = ("user__username", "organization__name")
    form = UserOrganizationMembershipForm
