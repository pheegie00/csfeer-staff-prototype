from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    name = "organizations"

    def ready(self):
        from django.db.models.signals import m2m_changed

        from organizations.models import UserOrganizationMembership
        from organizations.signals import (
            enforce_single_authorized_official,
        )

        m2m_changed.connect(
            enforce_single_authorized_official,
            sender=UserOrganizationMembership.groups.through,
        )
        m2m_changed.connect(
            enforce_single_authorized_official,
            sender=UserOrganizationMembership.permissions.through,
        )
