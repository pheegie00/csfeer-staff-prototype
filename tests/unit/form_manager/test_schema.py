from typing import cast

import pytest

from form_manager.schema.fields import TextField
from form_manager.schema.forms.base import (
    BaseFormFields,
)


def test_allowed_form_field_types():
    """Ensure that we can only add allowed field types to form field definitions."""

    with pytest.raises(AssertionError):

        class BadFormFields(BaseFormFields):

            first_name: str = "Steve"

            def _some_method(self):
                pass

    class GoodFormFields(BaseFormFields):

        first_name: TextField = cast(TextField, "Steve")

        def _some_method(self):
            pass
