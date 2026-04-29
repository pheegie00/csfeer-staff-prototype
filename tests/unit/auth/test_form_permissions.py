import pytest
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from csfeer.auth_backends.form_permissions import FormPermissionBackend
from users.permissions import ORG_PERMISSION_GROUPS
from users.signals import create_permission_groups


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ensure_custom_permissions_exist():
    """Create any custom model permissions that may be missing from the test DB.

    Permissions defined in Meta.permissions are normally created by
    create_permissions during migrate. With --reuse-db the DB may predate a
    permission being added, so we create them explicitly here.
    """
    for model in apps.get_models():
        ct = ContentType.objects.get_for_model(model)
        for codename, name in model._meta.permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={"name": name},
            )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def backend():
    return FormPermissionBackend()


@pytest.fixture
def permission_groups(db):
    """Seed Django groups matching ORG_PERMISSION_GROUPS, as post_migrate would."""
    _ensure_custom_permissions_exist()
    with patch("users.signals.create_permissions"):
        create_permission_groups(
            app_config=None,
            verbosity=0,
            interactive=False,
            using="default",
            plan=[],
        )


@pytest.fixture
def org(db):
    from organizations.models import OrganizationProfile

    return OrganizationProfile.objects.create(name="Test Org")


@pytest.fixture
def active_user(db, django_user_model):
    from faker import Faker

    fake = Faker()
    return django_user_model.objects.create_user(
        email=fake.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_active=True,
    )


@pytest.fixture
def inactive_user(db, django_user_model):
    from faker import Faker

    fake = Faker()
    return django_user_model.objects.create_user(
        email=fake.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_active=False,
    )


@pytest.fixture
def membership(active_user, org):
    from organizations.models import UserOrganizationMembership

    return UserOrganizationMembership.objects.create(user=active_user, organization=org)


@pytest.fixture
def form_edit_perm(db):
    _ensure_custom_permissions_exist()
    return Permission.objects.get(codename="form_edit")


@pytest.fixture
def form_view_perm(db):
    _ensure_custom_permissions_exist()
    return Permission.objects.get(codename="form_view")


# ---------------------------------------------------------------------------
# Early-exit guard tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_inactive_user_denied(backend, inactive_user, org):
    """Inactive users are always denied, regardless of membership or object."""
    from organizations.models import UserOrganizationMembership

    UserOrganizationMembership.objects.create(user=inactive_user, organization=org)
    assert backend.has_perm(inactive_user, "form_manager.form_edit", obj=org) is False


@pytest.mark.django_db
def test_obj_none_denied(backend, active_user):
    """has_perm returns False when no object is provided."""
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=None) is False


@pytest.mark.django_db
def test_non_org_obj_denied(backend, active_user):
    """has_perm returns False when obj is not an OrganizationProfile."""
    from django.contrib.auth.models import Group

    non_org_obj = Group.objects.create(name="not-an-org")
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=non_org_obj) is False


# ---------------------------------------------------------------------------
# Superuser bypass
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_superuser_granted_without_membership(backend, org, django_user_model):
    """Superusers are granted even when no membership row exists."""
    from faker import Faker

    fake = Faker()
    superuser = django_user_model.objects.create_superuser(
        email=fake.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    assert backend.has_perm(superuser, "form_manager.form_edit", obj=org) is True


@pytest.mark.django_db
def test_superuser_granted_for_any_perm(backend, org, django_user_model):
    """Superusers are granted regardless of which permission is checked."""
    from faker import Faker

    fake = Faker()
    superuser = django_user_model.objects.create_superuser(
        email=fake.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    assert backend.has_perm(superuser, "form_manager.nonexistent_perm", obj=org) is True


# ---------------------------------------------------------------------------
# No membership
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_no_membership_denied(backend, active_user, org):
    """Active non-superuser with no membership row is denied."""
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is False


@pytest.mark.django_db
def test_membership_for_different_org_denied(backend, active_user, org):
    """Membership for a different org does not grant access to this org."""
    from organizations.models import OrganizationProfile, UserOrganizationMembership

    other_org = OrganizationProfile.objects.create(name="Other Org")
    UserOrganizationMembership.objects.create(user=active_user, organization=other_org)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is False


# ---------------------------------------------------------------------------
# Direct (ad-hoc) permissions
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_direct_permission_granted(backend, active_user, org, membership, form_edit_perm):
    """A user with a matching direct permission on their membership is granted."""
    membership.permissions.add(form_edit_perm)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is True


@pytest.mark.django_db
def test_direct_permission_wrong_codename_denied(
    backend, active_user, org, membership, form_view_perm
):
    """A user with a direct permission for a different codename is denied."""
    membership.permissions.add(form_view_perm)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is False


@pytest.mark.django_db
def test_perm_without_app_label_resolves(backend, active_user, org, membership, form_edit_perm):
    """Codename resolution uses the last segment after '.', so bare codenames work too."""
    membership.permissions.add(form_edit_perm)
    assert backend.has_perm(active_user, "form_edit", obj=org) is True


@pytest.mark.django_db
def test_membership_with_no_permissions_denied(backend, active_user, org, membership):
    """A membership with no direct permissions and no groups is denied."""
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is False


# ---------------------------------------------------------------------------
# Group-based permissions
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_group_permission_granted(backend, active_user, org, membership, permission_groups):
    """A user in a group that has the permission is granted."""
    editor_group = Group.objects.get(name="Recipient Form Editor")
    membership.groups.add(editor_group)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is True


@pytest.mark.django_db
def test_group_without_permission_denied(backend, active_user, org, membership, permission_groups):
    """A user in a group that lacks the checked permission is denied."""
    # Viewer group only has form_view, not form_edit
    viewer_group = Group.objects.get(name="Recipient Form Viewer")
    membership.groups.add(viewer_group)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is False


@pytest.mark.django_db
def test_multiple_groups_one_matches(backend, active_user, org, membership, permission_groups):
    """A user in multiple groups is granted if any group has the permission."""
    viewer_group = Group.objects.get(name="Recipient Form Viewer")
    editor_group = Group.objects.get(name="Recipient Form Editor")
    membership.groups.add(viewer_group, editor_group)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is True


# ---------------------------------------------------------------------------
# Direct vs group — independence
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_direct_perm_without_group_still_granted(
    backend, active_user, org, membership, form_edit_perm
):
    """Direct permission alone is sufficient — no group needed."""
    membership.permissions.add(form_edit_perm)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is True


@pytest.mark.django_db
def test_group_perm_without_direct_still_granted(
    backend, active_user, org, membership, permission_groups
):
    """Group permission alone is sufficient — no direct permission needed."""
    editor_group = Group.objects.get(name="Recipient Form Editor")
    membership.groups.add(editor_group)
    assert backend.has_perm(active_user, "form_manager.form_edit", obj=org) is True
