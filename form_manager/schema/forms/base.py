"""Base form class definitions"""

import logging
from typing import (
    Annotated,
    Any,
    Generic,
    Optional,
    Sequence,
    TypeAlias,
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
from form_manager.schema.layout import SectionBlock, StepBlock

logger = logging.getLogger(__name__)


class ACFFormRenderer(TemplatesSetting):
    """A custom renderer"""

    form_template_name = "form_manager/forms/form.html"


class BaseFields(forms.Form):
    """A base Django form class that can also be used as a Pydantic field
    for serializing form defintions into base classes."""

    default_renderer = ACFFormRenderer

    def __init__(self, *args, ui_components=[], **kwargs):
        self.ui_components = ui_components
        super().__init__(*args, **kwargs)

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

    def get_context(self):
        """Set template context for rendering purposes."""
        context = cast(dict, super().get_context())

        # Recursively attach Django field objects to UI components
        # for rendering
        def attach_fields(node):
            if node["type"] == "field":
                field_name = node.get("field_name")
                field = self[field_name]
                node["django_field"] = field
            else:
                for child in node.get("children", []):
                    attach_fields(child)

        for component in self.ui_components:
            attach_fields(component)

        context.update({"ui_components": self.ui_components})

        return context


FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)

UIDefinition: TypeAlias = list[StepBlock]


class SchemaValidationError(Exception):
    form_class = None

    def __init__(self, message: str, form_class: Optional[object] = None):
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
    def dump_ui_definition_from_json_schema(
        cls, json_schema: Optional[dict[str, Any]] = None
    ) -> dict:
        """Dump the UI definition as a dictionary"""

        if not json_schema:
            json_schema = cls.model_json_schema()

        return json_schema["properties"]["ui"]["default"]
