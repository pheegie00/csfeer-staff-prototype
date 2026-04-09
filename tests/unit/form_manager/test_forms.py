from unittest.mock import Mock

import pytest
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

from form_manager.models import FormEntry
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields
from form_manager.schema.forms.utils import import_form_schema
from form_manager.utils import save_form_entry


def test_has_filter_fields():
    """Ensure the BaseForm.has_filter_fields method works."""

    class FormWithFilterField(BaseFields):

        item = acf_fields.FieldFilterField()

    class FormWithoutFilterField(BaseFields):

        item = acf_fields.CurrencyField()

    form_with = FormWithFilterField()
    form_without = FormWithoutFilterField()

    assert form_with.has_filter_fields is True
    assert form_without.has_filter_fields is False


def test_fields_to_exclude():
    """Ensure the BaseForm.fields_to_filter method works."""

    class FormWithFilterFields(BaseFields):

        item1_topics = acf_fields.FieldFilterField(
            choices=[
                ("field1,field2", "Topic1"),
                ("field3", "Topic 2"),
                ("field4,field5", "Topic 3"),
            ],
        )

        item2_topics = acf_fields.FieldFilterField(
            choices=[
                ("field6,field7", "Topic8"),
                ("field8,field9", "Topic 9"),
            ],
        )

    form = FormWithFilterFields(
        initial={
            "item1_topics": ["field1,field2", "field3"],
            "item2_topics": ["field6,field7"],
        }
    )

    assert set(form.fields_to_exclude) - set(["field4", "field5", "field8", "field9"]) == set()

    form = FormWithFilterFields()

    assert set(form.fields_to_exclude) - set([f"field{i+1}" for i in range(9)]) == set()


@pytest.mark.django_db
def test_save_form_entry_clears_field(form_entry: FormEntry, create_user):
    """Test that clearing a field value saves the empty value."""
    user, _ = create_user

    # Get the form class from the schema
    form_schema = import_form_schema(form_entry.form_definition.schema_class)
    form_class = form_schema.get_form_fields_class()

    # Step 1: Save initial data with a filled field
    request_mock = Mock()
    request_mock.user = user
    request_mock.POST = {
        "first_name": "John",
        "last_name": "Doe",
    }
    request_mock.FILES = {}

    save_form_entry(form_class, form_entry, request_mock)

    # Verify initial data was saved
    form_entry.refresh_from_db()
    assert form_entry.data["first_name"] == "John"
    assert form_entry.data["last_name"] == "Doe"

    # Step 2: Clear the first_name field
    request_mock.POST = {
        "first_name": "",  # Cleared field
        "last_name": "Doe",
    }

    save_form_entry(form_class, form_entry, request_mock)

    # Verify the cleared field was saved as empty string
    form_entry.refresh_from_db()
    assert form_entry.data["first_name"] == ""
    assert form_entry.data["last_name"] == "Doe"


@pytest.mark.django_db
def test_save_form_entry_excludes_calculated_fields(form_entry: FormEntry, create_user):
    """Test that calculated fields aren't overwritten from POST."""

    user, _ = create_user

    # Create mock request with calculated field value in POST
    request_mock = Mock()
    request_mock.user = user
    request_mock.POST = {
        "item1_cost": "50000",
        "item2_cost": "25000",
        "total_cost": "67",  # Bogus value - should be ignored
    }
    request_mock.FILES = {}

    form_schema = import_form_schema(form_entry.form_definition.schema_class)

    form_class = form_schema.get_form_fields_class()

    # Save the form entry
    save_form_entry(form_class, form_entry, request_mock)

    # Verify calculated field was NOT saved from POST
    form_entry.refresh_from_db()
    assert "total_cost" not in form_entry.data
    assert form_entry.data["item1_cost"] == "50,000.00"
    assert form_entry.data["item2_cost"] == "25,000.00"


@pytest.mark.django_db
def test_save_form_entry_handles_multiple_choice(form_entry: FormEntry, create_user):
    """Test that MultipleChoiceField values are properly saved."""
    user, _ = create_user

    # Create mock request with multiple selections
    request_mock = Mock()
    request_mock.user = user
    request_mock.POST = {
        "applicable_topics": ["item1_cost", "item2_cost"],  # Multiple values
    }
    request_mock.FILES = {}

    form_schema = import_form_schema(form_entry.form_definition.schema_class)

    form_class = form_schema.get_form_fields_class()

    # Save the form entry
    save_form_entry(form_class, form_entry, request_mock)

    # Verify list was saved correctly
    assert form_entry.data["applicable_topics"] == ["item1_cost", "item2_cost"]


@pytest.mark.django_db
def test_save_form_entry_handles_yesno_display_field(form_entry: FormEntry, create_user):
    """Test that ACFYesNoDisplayField (MultiValueField) is properly saved."""
    user, _ = create_user

    # Create mock request with MultiValueField POST data
    # YesNoDisplayField uses widget that creates has_funding_0, has_funding_1, etc.
    request_mock = Mock()
    request_mock.user = user
    request_mock.POST = {
        "extra_funding_0": "yes",  # Radio selection
        "extra_funding_1": "100.00",  # Amount field
    }
    request_mock.FILES = {}

    form_schema = import_form_schema(form_entry.form_definition.schema_class)

    form_class = form_schema.get_form_fields_class()

    # Save the form entry
    save_form_entry(form_class, form_entry, request_mock)

    # Verify MultiValueField was saved as compressed value
    assert "extra_funding" in form_entry.data
    # The field compresses to "yes-100.00" format
    assert form_entry.data["extra_funding"] == ["yes", "100.00"]


@pytest.mark.django_db
def test_save_form_entry_persists_uploaded_file_to_storage(
    form_entry: FormEntry, create_user, settings, tmp_path
):
    """Uploaded files are persisted and stored as storage paths in FormEntry.data."""
    user, _ = create_user

    settings.STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    settings.MEDIA_ROOT = str(tmp_path)

    class UploadForm(BaseFields):
        attachment = acf_fields.FileField(required=False)

    request_mock = Mock()
    request_mock.user = user
    request_mock.POST = {}
    request_mock.FILES = {
        "attachment": SimpleUploadedFile("tribal_resolution.pdf", b"test-pdf-bytes")
    }

    save_form_entry(UploadForm, form_entry, request_mock)
    form_entry.refresh_from_db()

    saved_path = form_entry.data.get("attachment")
    assert isinstance(saved_path, str)
    assert saved_path.startswith(f"form_uploads/{form_entry.pk}/attachment/")
    assert default_storage.exists(saved_path)
