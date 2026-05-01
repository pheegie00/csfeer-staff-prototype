import logging

from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from users.permissions import ALL_PERMISSIONS, ORG_PERMISSION_GROUPS

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_permission_groups(*args, **kwargs):
    """This signal handler creates the permission groups after the migrate command is complete."""

    # Don't create the groups if the permissions haven't been created in the db yet
    if Permission.objects.filter(codename__in=ALL_PERMISSIONS).count() < len(ALL_PERMISSIONS):
        return

    for group_name, codenames in ORG_PERMISSION_GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            logger.info(f"Created {group.name} auth group.")

        # Don't modify the permissions if they already exisist in teh group.
        existing_permissions = list(group.permissions.all().values_list("codename"))
        expected_permissions = Permission.objects.filter(codename__in=codenames)
        if set(existing_permissions) == set(expected_permissions.values_list("codename")):
            return

        group.permissions.set(expected_permissions)
        logger.info(
            f"Added {", ".join(expected_permissions.values_list("codename", flat=True))} "
            "to {group.name} auth group."
        )
