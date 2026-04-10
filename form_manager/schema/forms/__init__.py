from form_manager.schema.forms.base import BaseFormSchema
from form_manager.schema.forms.tribal_long_form import TribalLongForm
from form_manager.schema.forms.tribal_plan import TribalPlanForm
from form_manager.schema.forms.tribal_short_form import TribalShortForm

__all__ = [
    "BaseFormSchema",
    "TribalPlanForm",
    "TribalLongForm",
    "TribalShortForm",
]

ALL_FORM_SCHEMAS = [
    TribalPlanForm,
    TribalShortForm,
    TribalLongForm,
]
