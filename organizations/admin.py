from django.contrib import admin

from organizations.models import OrganizationProfile, UserOrganizationMembership


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone", "created_at")
    search_fields = ("name", "contact_email")


@admin.register(UserOrganizationMembership)
class UserOrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "user__email", "organization", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "organization__name")
