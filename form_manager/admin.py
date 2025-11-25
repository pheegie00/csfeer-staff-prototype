from django.contrib import admin

from .models import (
    FormAuditDetail,
    FormAuditTrail,
    FormDefinition,
    FormEntry,
    OrganizationProfile,
    UserOrganizationMembership,
)


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone", "created_at")
    search_fields = ("name", "contact_email")


@admin.register(UserOrganizationMembership)
class UserOrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "user__email", "organization", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "organization__name")


@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ("family", "name", "variant", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "variant", "family")


@admin.register(FormEntry)
class FormEntryAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "form_definition",
        "version_number",
        "status",
        "locked",
        "updated_at",
    )
    list_filter = ("status", "locked")
    search_fields = ("organization__name", "form_definition__name")


@admin.register(FormAuditTrail)
class FormAuditTrailAdmin(admin.ModelAdmin):
    list_display = ("form_entry", "user", "action", "timestamp")
    list_filter = ("action",)


@admin.register(FormAuditDetail)
class FormAuditDetailAdmin(admin.ModelAdmin):
    list_display = ("form_entry", "user", "user__email", "field_name", "timestamp")
    search_fields = ("field_name",)
    list_filter = ("form_entry__form_definition__name",)
