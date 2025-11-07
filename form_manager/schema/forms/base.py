"""Base form class definitions"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from ..layout import FieldBlock, SectionBlock


class BaseFormFields(BaseModel):
    """The base form fields object"""

    # To Do: figure out how to constrain this  base
    # class to only allow form field types


FormFields = TypeVar("FormFields", bound=BaseFormFields)
FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)


class BaseFormSchema(BaseModel, Generic[FormFields, FormId, FormVersion]):
    """The official schema for CSFEER form definitions."""

    id: FormId = Field(description="A unique slug for the form.")
    name: str = Field(description="The name of the form")
    version: FormVersion = Field(description="The form version")
    fields: FormFields = Field(
        description="Form field definitions. This should be a class that inherits BaseFormFields."
    )
    ui: list[SectionBlock | FieldBlock] = Field(description="The Form UI definition")
