"""Base form class definitions"""

import logging
from functools import cached_property
from typing import (
    Annotated,
    Any,
    Generic,
    TypeVar,
    cast,
    get_type_hints,
)

from django import forms
from django.forms.renderers import TemplatesSetting
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, FormFamilies
from form_manager.schema.fields import ACFBoundFieldFilterField, acf_fields

logger = logging.getLogger(__name__)


class ACFFormRenderer(TemplatesSetting):
    """A custom renderer"""

    form_template_name = "form_manager/forms/form.html"


class BaseFields(forms.Form):
    """A base Django form class that can also be used as a Pydantic field
    for serializing form defintions into base classes."""

    default_renderer = ACFFormRenderer

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """This is what allows us to used BaseFields as a pydantic type
        and continue to generate a JSON schema."""

        fields = {}

        for name, field in cls.declared_fields.items():

            try:
                fields[name] = field.to_pydantic_schema_type()  # type: ignore
            except Exception as error:
                logger.warning(error)
                continue

        return core_schema.typed_dict_schema(fields)

    def is_valid(self, use_default_if_excluded: bool = False) -> bool:
        """Validate the form.

        Args:
            use_default_if_empty: If True, fields with value_if_excluded will use
                that value for validation purposes. This happens by setting the value_if_excluded
                variable as the field value in the incoming data dictonary.

                This provides a way to validate the form when the user has excluded certain fields
                from the form interview.

        Returns:
            True if the form is valid, False otherwise.
        """
        if use_default_if_excluded:

            for name, instance in self.fields.items():
                if (
                    name in self.fields_to_exclude
                    and getattr(instance, "default_if_excluded", None) is not None
                ):
                    self.data[name] = instance.default_if_excluded  # type: ignore

        return super().is_valid()

    @cached_property
    def has_filter_fields(self) -> bool:
        """Return True if the form has any filter fields."""

        for _, field in self.fields.items():
            if isinstance(field, acf_fields.FieldFilterField):
                return True

        return False

    @cached_property
    def fields_to_exclude(self) -> list[str]:
        """Return a list of field names that should be excluded based on the filter fields."""

        fields_to_exclude = []

        for name, field in self.fields.items():
            if isinstance(field, acf_fields.FieldFilterField):
                bound_field = cast(ACFBoundFieldFilterField, self[name])
                fields_to_exclude += bound_field.get_fields_to_exclude()

        return fields_to_exclude


FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)

UIDefinition = type[list]


class SchemaValidationError(Exception):
    form_class = None

    def __init__(self, message: str, form_class: object | None = None):
        self.form_class = form_class
        super().__init__(message)


class BaseFormSchema(BaseModel, Generic[FormId, FormVersion], arbitrary_types_allowed=True):
    """The official schema for CSFEER form definitions."""

    family: FormFamilies = Field(description="The family of the form")
    name: Annotated[AllFormNames, Field(description="The name of the form")]
    variant: Annotated[
        SemanticVersion, Field(description="The version of the form", default="1.0.0")
    ]
    form_fields: BaseFields = Field(
        description="Form field definitions. This should be a class that inherits BaseFormFields."
    )
    ui: UIDefinition = Field(description="The Form UI definition")

    @classmethod
    def get_form_fields_class(cls) -> BaseFields | None:

        return get_type_hints(cls).get("form_fields")

    @classmethod
    def dump_ui_definition_from_json_schema(cls, json_schema: dict[str, Any] | None = None) -> dict:
        """Dump the UI definition as a dictionary"""

        if not json_schema:
            json_schema = cls.model_json_schema()

        return json_schema["properties"]["ui"]["default"]
