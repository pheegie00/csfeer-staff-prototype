from .base import BaseFormSchema
from .tribal_short_form import TribalShortForm
from .tribal_short_form_new_design import TribalShortFormNewDesign

__all__ = [
    "TribalShortForm",
    "BaseFormSchema",
    "TribalShortFormNewDesign",
]

ALL_FORM_SCHEMAS = [TribalShortForm, TribalShortFormNewDesign]
