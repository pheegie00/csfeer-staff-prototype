from form_manager.schema.forms.base import BaseFormSchema
from form_manager.schema.forms.tribal_long_form import TribalLongForm
from form_manager.schema.forms.tribal_short_form import TribalShortForm

__all__ = [
    "TribalLongForm",
    "TribalShortForm",
    "BaseFormSchema",
]

ALL_FORM_SCHEMAS = [TribalLongForm, TribalShortForm]
