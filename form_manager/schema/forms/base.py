"""Base form class definitions"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

from ..layout import FieldBlock, SectionBlock


class JSONSchemaService:
    """Utility class for working with JSON Schemas."""

    @classmethod
    def get_def_of_ref(cls, ref: str, schema: dict):
        path = ref.split("/")[1:]

        current = schema

        for part in path:
            current = current.get(part, {})

        return current


class BaseFormFields(BaseModel, arbitrary_types_allowed=True):
    """The base form fields object"""

    # To Do: figure out how to constrain this  base
    # class to only allow form field types


FormFields = TypeVar("FormFields", bound=BaseFormFields)
FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)


class BaseFormSchema(
    BaseModel, Generic[FormFields, FormId, FormVersion], arbitrary_types_allowed=True
):
    """The official schema for CSFEER form definitions."""

    id: FormId = Field(description="A unique slug for the form.")
    name: str = Field(description="The name of the form")
    version: FormVersion = Field(description="The form version")
    form_fields: FormFields = Field(
        description="Form field definitions. This should be a class that inherits BaseFormFields."
    )
    ui: list[SectionBlock | FieldBlock] = Field(description="The Form UI definition")

    @classmethod
    def dump_form_fields_from_json_schema(
        cls, json_schema: Optional[dict[str, Any]] = None
    ) -> dict | None:
        """Dump the form fields as a dictionary"""

        if not json_schema:
            json_schema = cls.model_json_schema()

        _def = JSONSchemaService.get_def_of_ref(
            json_schema["properties"]["form_fields"]["$ref"], json_schema
        )

        return _def.get("properties", None)

    @classmethod
    def dump_ui_definition_from_json_schema(
        cls, json_schema: Optional[dict[str, Any]] = None
    ) -> dict:
        """Dump the UI definition as a dictionary"""

        if not json_schema:
            json_schema = cls.model_json_schema()

        return json_schema["properties"]["ui"]["default"]

    @classmethod
    def merge_fields_into_ui_schema(cls, ui_schema: dict, form_fields: dict) -> dict:
        """Merge the form fields into the UI schema"""

        def merge_fields(component: dict) -> dict:

            if component.get("type") == "field":
                field_name = component.get("field_name")
                field_def = form_fields.get(field_name, {})
                component["field_definition"] = field_def

            if "children" in component:
                component["children"] = [merge_fields(child) for child in component["children"]]

            return component

        merged_ui = merge_fields(ui_schema)

        return merged_ui
