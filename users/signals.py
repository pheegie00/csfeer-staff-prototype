import logging

from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from users.permissions import ORG_PERMISSION_GROUPS

post_migrate.disconnect(
    create_permissions,
    dispatch_uid="django.contrib.auth.management.create_permissions",
)

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_permission_groups(*args, **kwargs):

    create_permissions(*args, **kwargs)

    for group_name, codenames in ORG_PERMISSION_GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            logger.info(f"Created {group.name} auth group.")
        permissions = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(permissions)
        logger.info(f"Added {permissions.values_list("codename")} to {group.name} auth group.")
