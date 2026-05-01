import pytest
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from users.permissions import ORG_PERMISSION_GROUPS
from users.signals import create_permission_groups


def _ensure_custom_permissions_exist():
    """Create any custom model permissions that may be missing from the test DB.

    Permissions defined in Meta.permissions are normally created by create_permissions
    during migrate. With --reuse-db the DB may predate a permission being added to a
    model without a corresponding AlterModelOptions migration (e.g. form_start on
    FormDefinition), so we create them explicitly here.
    """
    for model in apps.get_models():
        ct = ContentType.objects.get_for_model(model)
        for codename, name in model._meta.permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={"name": name},
            )


@pytest.fixture
def permission_groups(db):
    """Set up permission groups as post_migrate would, without depending on migration state."""
    _ensure_custom_permissions_exist()
    # Permissions are now in the DB; mock create_permissions to isolate group-creation logic.
    with patch("users.signals.create_permission_groups"):
        create_permission_groups(
            app_config=None,
            verbosity=0,
            interactive=False,
            using="default",
            plan=[],
        )


@pytest.mark.django_db
def test_all_permission_groups_exist(permission_groups):
    """All groups defined in ORG_PERMISSION_GROUPS exist after post_migrate."""
    existing = set(Group.objects.values_list("name", flat=True))
    for group_name in ORG_PERMISSION_GROUPS:
        assert group_name in existing, f"Group '{group_name}' was not created by post_migrate"


@pytest.mark.django_db
@pytest.mark.parametrize("group_name,expected_codenames", ORG_PERMISSION_GROUPS.items())
def test_permission_group_has_correct_permissions(
    permission_groups, group_name, expected_codenames
):
    """Each group has exactly the permissions defined in ORG_PERMISSION_GROUPS — no more, no less."""
    group = Group.objects.get(name=group_name)
    actual = set(group.permissions.values_list("codename", flat=True))
    assert actual == set(
        expected_codenames
    ), f"Group '{group_name}': expected {set(expected_codenames)}, got {actual}"


@pytest.mark.django_db
def test_create_permission_groups_signal_handler_creates_groups(permission_groups):
    """The signal handler re-creates groups with correct permissions when they are absent."""
    Group.objects.filter(name__in=ORG_PERMISSION_GROUPS.keys()).delete()

    with patch("users.signals.create_permission_groups"):
        create_permission_groups(
            app_config=None,
            verbosity=0,
            interactive=False,
            using="default",
            plan=[],
        )

    for group_name, expected_codenames in ORG_PERMISSION_GROUPS.items():
        assert Group.objects.filter(name=group_name).exists(), f"Group '{group_name}' not created"
        actual = set(
            Group.objects.get(name=group_name).permissions.values_list("codename", flat=True)
        )
        assert actual == set(expected_codenames)
