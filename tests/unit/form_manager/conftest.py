import pytest
from django.core.management import call_command
from organizations.models import OrganizationProfile
from form_manager.models import FormDefinition, FormEntry
from tests.unit.form_manager.fixtures.use_test_schema import use_test_schema


@pytest.fixture
def seed_data(create_user, use_test_schema):
    user, details = create_user

    call_command("seed_demo_org", email=user.email, all=True)
    call_command("load_initial_forms")

    return user, details


@pytest.fixture
def form_entry(seed_data, create_user) -> FormEntry:

    user, user_details = create_user

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    form_def = FormDefinition.objects.first()

    entry = FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=user, version_number="1"
    )

    return entry
