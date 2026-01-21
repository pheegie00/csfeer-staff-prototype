from functools import cached_property
from typing import Annotated, Any, Generic, TypeAlias, TypeVar

from _typeshed import Incomplete
from django import forms
from django.forms.boundfield import BoundField
from django.forms.renderers import TemplatesSetting
from django.forms.utils import ErrorList
from pydantic import BaseModel
from pydantic import GetCoreSchemaHandler as GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_extra_types.semantic_version import SemanticVersion as SemanticVersion

from form_manager.constants import AllFormNames as AllFormNames
from form_manager.constants import FormFamilies as FormFamilies
from form_manager.schema.fields import acf_fields
from form_manager.schema.layout import SectionBlock, StepBlock

logger: Incomplete

class PydanticErrorList(ErrorList):
    template_name: str
    template_name_text: str
    template_name_ul: str

class ACFFormRenderer(TemplatesSetting):
    form_template_name: str
    formset_template_name: str
    field_template_name: str

FOO = TypeVar("FOO")

class BaseFields(forms.Form):
    default_renderer = ACFFormRenderer
    ui_components: Incomplete
    def __init__(self, *args, ui_components=[], **kwargs) -> None: ...
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema: ...
    def get_context(self): ...
    @cached_property
    def has_filter_fields(self) -> bool: ...
    @cached_property
    def fields_to_exclude(self) -> list[str]: ...

FormId = TypeVar("FormId", bound=str)
FormVersion = TypeVar("FormVersion", bound=str)

UIDefinition: TypeAlias = list[StepBlock | SectionBlock]

class SchemaValidationError(Exception):
    form_class: Incomplete
    def __init__(self, message: str, form_class: object | None = None) -> None: ...

class BaseFormSchema(BaseModel, Generic[FormId, FormVersion], arbitrary_types_allowed=True):
    family: FormFamilies
    name: Annotated[AllFormNames, None]
    variant: Annotated[SemanticVersion, None]
    form_fields: BaseFields
    ui: UIDefinition
    @classmethod
    def get_form_fields_class(cls) -> BaseFields | None: ...
    @classmethod
    def dump_ui_definition_from_json_schema(
        cls, json_schema: dict[str, Any] | None = None
    ) -> dict: ...
