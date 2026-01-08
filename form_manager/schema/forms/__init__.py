from .base import BaseFormSchema
from .tribal_long_form import TribalLongForm

__all__ = [
    "TribalLongForm",
    "BaseFormSchema",
]

ALL_FORM_SCHEMAS = [TribalLongForm]
