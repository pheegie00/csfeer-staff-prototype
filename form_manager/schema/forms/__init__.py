from .base import BaseFormSchema
from .tribal_short_form import TribalShortForm

__all__ = [
    "TribalShortForm",
    "BaseFormSchema",
]

ALL_FORM_SCHEMAS = [TribalShortForm]
