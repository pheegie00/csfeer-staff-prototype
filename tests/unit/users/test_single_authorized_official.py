import pytest
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from users.permissions import ORG_PERMISSION_GROUPS
from users.signals import create_permission_groups


def _ensure_custom_permissions_exist():
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
def ao_group(permission_groups):
    return Group.objects.get(name="Recipient Authorized Official")


@pytest.fixture
def make_user(db, django_user_model):
    from faker import Faker

    fake = Faker()

    def _make():
        return django_user_model.objects.create_user(
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_active=True,
        )

    return _make


@pytest.mark.django_db
def test_first_authorized_official_is_allowed(org, ao_group, make_user):
    """The first AO assignment for an org succeeds without error."""
    from organizations.models import UserOrganizationMembership

    membership = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    membership.groups.add(ao_group)  # must not raise
    assert membership.groups.filter(name="Recipient Authorized Official").exists()


@pytest.mark.django_db
def test_second_authorized_official_is_blocked(org, ao_group, make_user):
    """Adding a second AO to the same org raises ValidationError."""
    from organizations.models import UserOrganizationMembership

    m1 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    m1.groups.add(ao_group)

    m2 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    with pytest.raises(ValidationError, match="already has a Recipient Authorized Official"):
        m2.groups.add(ao_group)


@pytest.mark.django_db
def test_ao_in_different_orgs_is_allowed(ao_group, make_user, db):
    """Each org may have its own AO — the constraint is per-organization."""
    from organizations.models import OrganizationProfile, UserOrganizationMembership

    org_a = OrganizationProfile.objects.create(name="Org A")
    org_b = OrganizationProfile.objects.create(name="Org B")

    m_a = UserOrganizationMembership.objects.create(user=make_user(), organization=org_a)
    m_b = UserOrganizationMembership.objects.create(user=make_user(), organization=org_b)

    m_a.groups.add(ao_group)  # must not raise
    m_b.groups.add(ao_group)  # must not raise — different org


@pytest.mark.django_db
def test_reassigning_same_member_does_not_block(org, ao_group, make_user):
    """Re-adding the AO group to a membership that already holds it is idempotent."""
    from organizations.models import UserOrganizationMembership

    membership = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    membership.groups.add(ao_group)
    membership.groups.add(ao_group)  # second add must not raise


@pytest.mark.django_db
def test_non_ao_groups_are_unaffected(org, make_user, permission_groups):
    """Multiple members can share non-AO groups without triggering the constraint."""
    from organizations.models import UserOrganizationMembership

    editor_group = Group.objects.get(name="Recipient Form Editor")

    m1 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    m2 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)

    m1.groups.add(editor_group)
    m2.groups.add(editor_group)  # must not raise


# ---------------------------------------------------------------------------
# Direct permission assignment constraint
# ---------------------------------------------------------------------------


@pytest.fixture
def ao_permission(db):
    from django.contrib.auth.models import Permission
    from organizations.signals import AO_PERMISSION_CODENAME

    return Permission.objects.get(codename=AO_PERMISSION_CODENAME)


@pytest.mark.django_db
def test_direct_ao_permission_blocked_when_another_has_it_directly(org, ao_permission, make_user):
    """Directly assigning the AO permission to a second member is blocked."""
    from organizations.models import UserOrganizationMembership

    m1 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    m1.permissions.add(ao_permission)

    m2 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    with pytest.raises(ValidationError, match="already has a Recipient Authorized Official"):
        m2.permissions.add(ao_permission)


@pytest.mark.django_db
def test_direct_ao_permission_blocked_when_another_has_ao_group(
    org, ao_group, ao_permission, make_user
):
    """Directly assigning the AO permission is blocked when another member holds it via the AO group."""
    from organizations.models import UserOrganizationMembership

    m1 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    m1.groups.add(ao_group)

    m2 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    with pytest.raises(ValidationError, match="already has a Recipient Authorized Official"):
        m2.permissions.add(ao_permission)


@pytest.mark.django_db
def test_ao_group_blocked_when_another_has_direct_permission(
    org, ao_group, ao_permission, make_user
):
    """Adding the AO group is blocked when another member already holds the permission directly."""
    from organizations.models import UserOrganizationMembership

    m1 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    m1.permissions.add(ao_permission)

    m2 = UserOrganizationMembership.objects.create(user=make_user(), organization=org)
    with pytest.raises(ValidationError, match="already has a Recipient Authorized Official"):
        m2.groups.add(ao_group)
