import pytest
from django.core.management import call_command
from organizations.models import OrganizationProfile
from form_manager.models import FormDefinition, FormEntry
from tests.unit.form_manager.fixtures.use_test_schema import use_test_schema


@pytest.fixture
def empty_form_definitions(db):
    """Clear FormDefinition/FormEntry rows pre-seeded by CI's load_initial_forms.

    Why: setup-tests-ci runs `load_initial_forms` against the same DB pytest
    reuses (--reuse-db), so canonical rows are visible to tests that assume an
    empty table. Deletes happen inside the test transaction and are rolled back.
    """
    FormEntry.objects.all().delete()
    FormDefinition.objects.all().delete()


@pytest.fixture
def seed_data(create_user, use_test_schema):
    user = create_user

    call_command("load_initial_forms")

    return user


@pytest.fixture
def form_entry(seed_data, create_user) -> FormEntry:

    user = create_user

    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()

    form_def = FormDefinition.objects.first()

    entry = FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=user, version_number="1"
    )

    return entry
