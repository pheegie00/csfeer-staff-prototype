from unittest.mock import Mock

import pytest
from django.forms import MultipleChoiceField

from form_manager.models import FormEntry
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields
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
    form_schema = form_entry.form_definition.get_schema()
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
def test_save_form_entry_excludes_calculated_fields():
    """Test that calculated fields aren't overwritten from POST."""
    from form_manager.schema.fields import ACFCalculatedCurrencyField

    # Create a test form with a calculated field
    class TestFormWithCalculated(BaseFields):
        employment = acf_fields.CurrencyField(title="Employment")
        housing = acf_fields.CurrencyField(title="Housing")
        total_expenditures = ACFCalculatedCurrencyField(
            title="Total", fields=["employment", "housing"]
        )

    # Create mock form entry
    form_entry = Mock()
    form_entry.data = {}

    # Create mock request with calculated field value in POST
    request_mock = Mock()
    request_mock.user = Mock()
    request_mock.POST = {
        "employment": "50000",
        "housing": "25000",
        "total_expenditures": "999999",  # Bogus value - should be ignored
    }
    request_mock.FILES = {}

    # Initialize the form to get the calculated value
    form = TestFormWithCalculated(request_mock.POST)

    # Save the form entry
    save_form_entry(TestFormWithCalculated, form_entry, request_mock)

    # Verify calculated field was NOT saved from POST
    assert "total_expenditures" not in form_entry.data
    assert form_entry.data["employment"] == "50000.00"
    assert form_entry.data["housing"] == "25000.00"


@pytest.mark.django_db
def test_save_form_entry_handles_multiple_choice():
    """Test that MultipleChoiceField values are properly saved."""

    # Create a test form with a MultipleChoiceField
    class TestFormWithMultipleChoice(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("topic1", "Topic 1"),
                ("topic2", "Topic 2"),
                ("topic3", "Topic 3"),
            ]
        )

    # Create mock form entry
    form_entry = Mock()
    form_entry.data = {}

    # Create mock request with multiple selections
    request_mock = Mock()
    request_mock.user = Mock()
    request_mock.POST = {
        "topics": ["topic1", "topic3"],  # Multiple values
    }
    request_mock.FILES = {}

    # Save the form entry
    save_form_entry(TestFormWithMultipleChoice, form_entry, request_mock)

    # Verify list was saved correctly
    assert form_entry.data["topics"] == ["topic1", "topic3"]


@pytest.mark.django_db
def test_save_form_entry_handles_yesno_display_field():
    """Test that ACFYesNoDisplayField (MultiValueField) is properly saved."""
    from form_manager.schema.fields import ACFYesNoDisplayField

    # Create a test form with a YesNoDisplayField
    class TestFormWithYesNo(BaseFields):
        has_funding = ACFYesNoDisplayField(
            fields=[
                acf_fields.CurrencyField(title="Funding Amount"),
            ],
            title="Do you have funding?",
        )

    # Create mock form entry
    form_entry = Mock()
    form_entry.data = {}

    # Create mock request with MultiValueField POST data
    # YesNoDisplayField uses widget that creates has_funding_0, has_funding_1, etc.
    request_mock = Mock()
    request_mock.user = Mock()
    request_mock.POST = {
        "has_funding_0": "yes",  # Radio selection
        "has_funding_1": "100.00",  # Amount field
    }
    request_mock.FILES = {}

    # Save the form entry
    save_form_entry(TestFormWithYesNo, form_entry, request_mock)

    # Verify MultiValueField was saved as compressed value
    assert "has_funding" in form_entry.data
    # The field compresses to "yes-100.00" format
    assert form_entry.data["has_funding"] == "yes-100.00"
