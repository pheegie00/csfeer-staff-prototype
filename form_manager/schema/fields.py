"""Form field definitions."""

from __future__ import annotations

import inspect
from datetime import date, datetime
from decimal import Decimal
from typing import List

from django import forms
from django.forms.boundfield import BoundField
from django.utils.functional import cached_property
from pydantic_core import core_schema


class ACFFieldMixin:
    title: str | None = None
    description: str | None = None

    def __init__(self, *args, title=None, description=None, **kwargs):
        self.title = kwargs.pop("title", None)
        self.description = kwargs.pop("description", None)
        kwargs["help_text"] = kwargs.get("help_text", description)
        super().__init__(*args, **kwargs)

    def to_pydantic_schema_type(self):
        """Convert this field to a pydantic schema type."""

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


class ACFCalculatedField(ACFFieldMixin, forms.FloatField):
    """A field whose value is calculated from other form fields."""

    fields: List[str]

    class ACFCalculatedBoundField(BoundField):
        """A BoundField for Calculated Fields."""

        field: ACFCalculatedField  # type: ignore

        @property
        def data(self):
            """
            Return the data for this BoundField, or None if it wasn't given.
            """
            values = []

            for source_field in self.field.fields:
                source_value = self.form.data.get(source_field)
                if source_value in (None, ""):
                    continue
                values.append(float(source_value))

            return sum(values)

        @cached_property
        def initial(self):
            """Overload the initial property to always return the calcualted value."""

            return self.data

    def __init__(self, *args, fields: List[str], **kwargs):

        self.fields = fields
        kwargs.update(
            {"disabled": True, "bound_field_class": self.ACFCalculatedBoundField, "required": False}
        )
        super().__init__(*args, **kwargs)


class ACFCalculatedCurrencyField(ACFCalculatedField):
    pass


class ACFCurrencyField(ACFFieldMixin, forms.FloatField):
    pass


class ACFTextAreaField(ACFFieldMixin, forms.CharField):
    pass


class ACFPhoneNumberField(ACFFieldMixin, forms.CharField):
    pass


class ACFFieldsMeta(type):

    def __new__(cls, name, bases=(), dct={}):

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
                "TextareaField": ACFTextAreaField,
                "PhoneNumberField": ACFPhoneNumberField,
                "CalculatedCurrencyField": ACFCalculatedCurrencyField,
                "CalculatedField": ACFCalculatedField,
            }
        )

        return super().__new__(cls, name, bases, dct)


class acf_fields(metaclass=ACFFieldsMeta): ...
