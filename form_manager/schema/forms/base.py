"""Base form class definitions"""

from typing import (
    Annotated,
    Any,
    Generic,
    Optional,
    Tuple,
    TypeVar,
    cast,
    get_type_hints,
)

from django import forms
from django.forms.renderers import TemplatesSetting
from django.forms.utils import ErrorList
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, FormFamilies
from form_manager.schema.layout import FieldBlock, SectionBlock


class PydanticErrorList(ErrorList):
    """A custom error renderer"""

    template_name = "form_manager/forms/error_list.html"
    template_name_text = "form_manager/forms/error_list_text.txt"
    template_name_ul = "form_manager/forms/error_list_ul.html"


class ACFFormRenderer(TemplatesSetting):
    """A custom renderer"""

    form_template_name = "form_manager/forms/form.html"
    formset_template_name = "form_manager/forms/formset.html"
    field_template_name = "form_manager/forms/field.html"


class JSONSchemaService:
    """Utility class for working with JSON Schemas."""

    @classmethod
    def get_def_of_ref(cls, ref: str, schema: dict):
        path = ref.split("/")[1:]

        current = schema

        for part in path:
            current = current.get(part, {})

        return current


class BaseFields(forms.Form):
    """A base form class for form fields."""

    default_renderer = ACFFormRenderer

    def __init__(self, *args, ui_components=None, **kwargs):
        self.ui_components = ui_components
        super().__init__(*args, **kwargs)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:

        fields = {}

        for name, field in cls.declared_fields.items():

            try:

                fields[name] = field.to_pydantic_schema_type()
            except Exception as error:
                print(error)
                continue

        return core_schema.typed_dict_schema(fields)

    def get_context(self):

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


FormFields = TypeVar("FormFields", bound=BaseFields)
FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)


class SchemaValidationError(Exception):
    form_class = None

    def __init__(self, message: str, form_class: Optional[object] = None):
        self.form_class = form_class
        super().__init__(message)


class BaseFormSchema(
    BaseModel, Generic[FormFields, FormId, FormVersion], arbitrary_types_allowed=True
):
    """The official schema for CSFEER form definitions."""

    family: FormFamilies = Field(description="The family of the form")
    name: Annotated[AllFormNames, Field(description="The name of the form")]
    variant: Annotated[
        SemanticVersion, Field(description="The version of the form", default="1.0.0")
    ]
    form_fields: Any = Field(
        description="Form field definitions. This should be a class that inherits BaseFormFields."
    )
    ui: list[SectionBlock | FieldBlock] = Field(description="The Form UI definition")

    # @classmethod
    # def model_json_schema(cls, *args, **kwargs):
    #     """Overload this method to perform some schema validation."""

    #     for field in ["family", "name", "variant"]:
    #         if not cls.model_fields[field].frozen:
    #             raise SchemaValidationError(
    #                 f"Field {field} in {cls.__name__} must have frozen=True", form_class=cls
    #             )

    #     return super().model_json_schema()

    @classmethod
    def dump_form_fields_from_json_schema(
        cls, json_schema: Optional[dict[str, Any]] = None
    ) -> Tuple[dict | None, list[str]]:
        """Dump the form fields as a dictionary"""

        if not json_schema:
            json_schema = cls.model_json_schema()

        _def = JSONSchemaService.get_def_of_ref(
            json_schema["properties"]["form_fields"]["$ref"], json_schema
        )

        return _def.get("properties", None), _def.get("required", [])

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

    # @classmethod
    # def merge_fields_into_ui_schema(cls, ui_schema: dict, form_fields: dict) -> dict:
    #     """Merge the form fields into the UI schema"""

    #     def merge_fields(component: dict) -> dict:

    #         if component.get("type") == "field":
    #             field_name = component.get("field_name")
    #             field_def = form_fields.get(field_name, {})
    #             component["field_definition"] = field_def

    #         if "children" in component:
    #             component["children"] = [merge_fields(child) for child in component["children"]]

    #         return component

    #     merged_ui = merge_fields(ui_schema)

    #     return merged_ui
