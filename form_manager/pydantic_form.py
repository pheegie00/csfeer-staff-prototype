import logging
from typing import cast

from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.renderers import TemplatesSetting
from django.forms.utils import ErrorList

from .schema.forms.base import BaseFormSchema

logger = logging.getLogger(__name__)


class PydanticErrorList(ErrorList):
    """A custom error renderer"""

    template_name = "form_manager/forms/error_list.html"
    template_name_text = "form_manager/forms/error_list_text.txt"
    template_name_ul = "form_manager/forms/error_list_ul.html"


class PydantiJSONSchemaFormRenderer(TemplatesSetting):
    """A custom renderer"""

    form_template_name = "form_manager/forms/form.html"
    formset_template_name = "form_manager/forms/formset.html"
    field_template_name = "form_manager/forms/field.html"


class PyddanticDeclarativeFieldsMetaclass(DeclarativeFieldsMetaclass):
    """This is a metaclass that creates and attaches django form fields
    to a django form class from a pydantic schema."""

    _schema = None

    def __new__(cls, name, bases, attrs):

        _schema = attrs.pop("_schema", None)

        if _schema:
            new_attrs = cls._generate_django_form_fields(_schema)
            attrs = attrs | {"_schema": _schema} | new_attrs

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def _generate_django_form_fields(cls, _schema: dict | None):
        form_attrs = {}

        form_fields, required_fields = BaseFormSchema.dump_form_fields_from_json_schema(_schema)

        if not form_fields:
            return form_attrs

        for name, field in form_fields.items():
            # Build the field
            label = field.get("title", name)
            required = name in required_fields
            help_text = field.get("description", "")
            # field_type = field_def.get("type", "text")
            max_length = field.get("maxLength")
            min_length = field.get("minLength")
            field_type = field.get("fieldType", None)
            field_object = None

            if field_type == "TextField":
                field_object = forms.CharField(
                    label=label,
                    required=required,
                    help_text=help_text,
                    max_length=max_length,
                )
            elif field_type == "EmailField":
                field_object = forms.EmailField(
                    label=label,
                    required=required,
                    help_text=help_text,
                )
            elif field_type == "PhoneNumberField":
                field_object = forms.CharField(
                    label=label,
                    required=required,
                    help_text=help_text,
                    max_length=max_length,
                    min_length=min_length,
                )
            elif field_type == "CurrencyField":
                field_object = forms.FloatField(
                    label=label,
                    required=required,
                    help_text=help_text,
                )
            elif field_type == "TextareaField":
                field_object = forms.CharField(
                    label=label,
                    required=required,
                    help_text=help_text,
                    widget=forms.Textarea,
                )
            elif field_type == "ComputedField":
                field_object = forms.CharField(
                    label=label,
                    required=required,
                    help_text=help_text,
                    disabled=True,
                )
            else:
                logger.warning(f"Unsupported field type: {field_type} for field {name}")

            if field_object:
                form_attrs[name] = field_object

        return form_attrs


class PydanticJSONSchemaForm(forms.BaseForm, metaclass=PyddanticDeclarativeFieldsMetaclass):
    """A Django form generated from a Pydantic json schema"""

    _schema = None

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "renderer": PydantiJSONSchemaFormRenderer(),
                "error_class": PydanticErrorList,
            }
        )
        super().__init__(*args, **kwargs)

    def get_context(self):
        context = cast(dict, super().get_context())

        ui_components = BaseFormSchema.dump_ui_definition_from_json_schema(self._schema)

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

        for component in ui_components:
            attach_fields(component)

        context.update({"ui_components": ui_components})

        return context
