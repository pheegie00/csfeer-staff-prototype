"""Form field definitions."""

from __future__ import annotations

import inspect
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, List

from django import forms
from django.forms.boundfield import BoundField
from pydantic_core import core_schema

from form_manager.schema.widgets import CheckboxSelectMultiple, CurrencyInput


class ACFFieldMixin:
    """A mixin class that provides some common ACF field functionality and makes
    standard Django form fields usable in pydantic classes."""

    title: str | None = None
    description: str | None = None

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop("title", None)
        self.description = kwargs.pop("description", None)
        kwargs["help_text"] = kwargs.get("help_text", self.description)
        super().__init__(*args, **kwargs)

    def to_pydantic_schema_type(self):
        """Convert the field to a pydantic schema type when using Pydantic to serialize
        the form definition into json.

        To Do: This will only provide very basic field info at the moment. If we intend to
        make the JSON schema the source of truth for form definitions, we will need to
        include more field properties in the dumped schema.
        """

        field_type_map = {
            "BooleanField": bool,
            "DateField": date,
            "DateTimeField": datetime,
            "DecimalField": Decimal,
            "FloatField": float,
            "JSONField": dict,
            "CurrencyField": float,
            "CalculatedField": float,
            "CalculatedCurrencyField": float,
        }

        _type = field_type_map.get(self.__class__.__name__) or field_type_map.get(
            self.__class__.__name__.replace("ACF", ""), str
        )

        extra_fields = [
            "title",
            "description",
            "max_length",
            "min_length",
            "required",
            "label",
            "initial",
            "max_value",
            "min_value",
            "step_size",
            "max_digits",
            "decimal_places",
        ]

        data = {
            f: getattr(self, f, None) for f in extra_fields if getattr(self, f, None) is not None
        }

        field_type_schema = getattr(core_schema, f"{_type.__name__}_schema")
        possible_args = inspect.getcallargs(field_type_schema).keys()
        data_args = {k: v for k, v in data.items() if k in possible_args}

        return core_schema.typed_dict_field(field_type_schema(**data_args))


class ACFCurrencyField(ACFFieldMixin, forms.FloatField):
    """A currency field"""

    widget = CurrencyInput

    def __init__(self, *args, **kwargs):
        step_size = kwargs.pop("step_size", 0.01)
        super().__init__(*args, step_size=step_size, **kwargs)

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update(
            {
                "class": "usa-input currency-input",
            }
        )
        return attrs


class ACFCalculatedField(ACFFieldMixin, forms.FloatField):
    """A field whose value is calculated from other form fields."""

    fields: List[str]

    class ACFCalculatedBoundField(BoundField):
        """A BoundField for Calculated Fields."""

        field: ACFCalculatedField  # type: ignore

        @property
        def data(self):
            """
            Sum the values of the source fields.
            """
            values = []

            for source_field in self.field.fields:
                source_value = self.form.data.get(source_field)
                if source_value in (None, ""):
                    continue
                values.append(float(source_value))

            return sum(values)

        @property
        def initial(self):
            initial = self.form.get_initial_for_field(self.field, self.name)

            return self.data or initial

    bound_field_class = ACFCalculatedBoundField

    def __init__(self, *args, fields: List[str], **kwargs):
        """Overloaded to set the source field list and the disabled and required attributes."""
        self.fields = fields
        kwargs.update({"disabled": True, "required": False})
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        """Overloaded to return the calculated value even if
        the field is disabled."""

        return data or initial

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update(
            {
                "class": "usa-input calculated-field",
                "data-source-fields": ",".join(self.fields),
            }
        )
        return attrs


class ACFCalculatedCurrencyField(ACFCalculatedField, ACFCurrencyField):
    """A calculated currency field"""

    widget = CurrencyInput()

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update({"class": attrs.get("class", "") + " calculated-currency-field"})
        return attrs


class ACFTextareaField(ACFFieldMixin, forms.CharField):
    """A text area field"""

    widget = forms.Textarea


class FieldFilterField(ACFFieldMixin, forms.MultipleChoiceField):
    """A special field that defines fields to exclude from interview questions."""

    widget = CheckboxSelectMultiple


class ACFFieldsMeta(type):

    def __new__(cls, name, bases=(), dct={}):
        """A metaclass that creates an object of custom ACF form fields from built-in Django
        form fields. They're all accessible on the acf_fields object below."""

        for name, field_class in forms.fields.__dict__.items():

            try:
                if not issubclass(field_class, forms.Field):
                    continue
            except TypeError:
                continue

            dct.update({name: type(name, (ACFFieldMixin, field_class), {})})

        dct.update(
            {
                "CurrencyField": ACFCurrencyField,
                "TextareaField": ACFTextareaField,
                "CalculatedCurrencyField": ACFCalculatedCurrencyField,
                "CalculatedField": ACFCalculatedField,
                "PageFilterField": FieldFilterField,
            }
        )

        return super().__new__(cls, name, bases, dct)


class acf_fields(metaclass=ACFFieldsMeta): ...
