from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import (
    BaseFields,
)


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


def test_fields_to_filter():
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

    assert form.fields_to_filter == ["field1", "field2", "field3", "field6", "field7"]

    form = FormWithFilterFields()

    assert form.fields_to_filter == []
