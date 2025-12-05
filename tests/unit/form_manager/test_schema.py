import pytest

from form_manager.schema.fields import TextField
from form_manager.schema.forms.base import (
    BaseFormFields,
    BaseFormSchema,
    FieldBlock,
    FormFamilies,
    SectionBlock,
)


def test_allowed_form_field_types():
    """Ensure that we can only add allowed field types to form field definitions."""

    class BadFormFields(BaseFormFields):

        first_name: str = "Steve"

        def _some_method(self):
            pass

    with pytest.raises(AssertionError):

        BadFormFields.model_json_schema()

    class GoodFormFields(BaseFormFields):

        first_name: TextField = "Steve"

        def _some_method(self):
            pass

    GoodFormFields.model_json_schema()
