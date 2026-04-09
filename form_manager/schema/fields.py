"""Form field definitions."""

from __future__ import annotations

import inspect
from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, cast

from django import forms
from django.forms.boundfield import BoundField
from django.utils import formats
from pydantic_core import core_schema

from form_manager.schema.widgets import (
    ACFCheckboxInput,
    CheckboxSelectMultiple,
    CurrencyInput,
    YesNoDisplayWidget,
)

if TYPE_CHECKING:
    from form_manager.schema.forms.base import BaseFields


class ACFFieldMixin:
    """A mixin class that provides some common ACF field functionality and makes
    standard Django form fields usable in pydantic classes.
    """

    title: str | None = None
    """Human-friendly short title for the field. Typically used as the label shown
    on forms and in review screens."""

    review_title: str | None = None
    """Description of the field to be displayed on the review page."""

    description: str | None = None
    """Longer descriptive text or help/auxiliary information for the field. This
    is commonly used as the Django form `help_text` and can guide users."""

    is_presentational_only: bool = False
    """If True, the field is presentational only and does not represent user
    input that should be persisted or used for business logic (e.g. decorative
    headings or separators)."""

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop("title", None)
        self.description = kwargs.pop("description", None)
        self.is_presentational_only = kwargs.pop("is_presentational_only", False)
        self.review_title = kwargs.pop("review_title", False)
        self.default_if_excluded = kwargs.pop("default_if_excluded", None)

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
            "CalculatedDecimalField": float,
            "CalculatedIntegerField": int,
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
            "value_if_excluded",
        ]

        data = {
            f: getattr(self, f, None) for f in extra_fields if getattr(self, f, None) is not None
        }

        field_type_schema = getattr(core_schema, f"{_type.__name__}_schema")
        possible_args = inspect.getcallargs(field_type_schema).keys()
        data_args = {k: v for k, v in data.items() if k in possible_args}

        return core_schema.typed_dict_field(field_type_schema(**data_args))


class ACFField(ACFFieldMixin, forms.Field): ...


class ACFIntegerField(ACFFieldMixin, forms.IntegerField):
    """An integer field with comma formatting."""

    widget = forms.TextInput

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update(
            {
                "class": "usa-input integer-input",
                "inputmode": "numeric",
                "x-mask:dynamic": "$money($input, '.', ',', 0)",
            }
        )
        return attrs

    def to_python(self, value):
        """Strip commas from the input before validation."""
        if isinstance(value, str):
            value = value.replace(",", "")
        return super().to_python(value)

    def prepare_value(self, value):
        """Format the value with comma separators for display."""
        if value in [None, ""]:
            return ""
        try:
            return formats.number_format(int(value), 0, True)
        except (ValueError, TypeError):
            return value


class ACFCurrencyField(ACFFieldMixin, forms.DecimalField):
    """A currency field"""

    widget = CurrencyInput

    def __init__(self, *args, **kwargs):
        kwargs.update({"decimal_places": 2, "localize": True})
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update(
            {
                "class": "usa-input currency-input",
                "x-mask:dynamic": "$money($input, '.', ',')",
            }
        )
        return attrs

    def prepare_value(self, value):
        """Format the value as a currency string for display in the form field."""
        # value = value or "0.00"
        if value in [None, ""]:
            return ""
        sanitized = formats.sanitize_separators(value)
        return formats.number_format(sanitized, 2, True)


class ACFCalculatedFieldMixin(ACFFieldMixin, forms.Field):

    fields: list[str]

    class ACFCalculatedBoundField(BoundField):
        """A BoundField for Calculated Fields."""

        field: ACFCalculatedFieldMixin  # type: ignore
        form: BaseFields  # type: ignore

        def get_calculated_value(self):
            """
            Sum the values of the source fields.
            """
            values = []

            fields_to_exclude = self.form.fields_to_exclude

            for field_name in self.field.fields:

                if field_name in fields_to_exclude:
                    continue

                source_field = self.form[field_name]
                source_value = source_field.value()

                if source_value in (None, ""):
                    continue

                sanitized = formats.sanitize_separators(source_value)

                values.append(Decimal(sanitized))

            return sum(values)

        @property
        def data(self):
            return self.get_calculated_value()

        @property
        def initial(self):
            return self.get_calculated_value()

    bound_field_class = ACFCalculatedBoundField

    def __init__(self, *args, fields: list[str], **kwargs):
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
                "type": "text",
            }
        )
        return attrs


class ACFCalculatedIntegerField(ACFCalculatedFieldMixin, ACFIntegerField):
    pass


class ACFCalculatedDecimalField(ACFCalculatedFieldMixin, forms.DecimalField):
    """A field whose value is calculated from other form fields."""

    pass


class ACFCalculatedCurrencyField(ACFCalculatedDecimalField, ACFCurrencyField):
    """A calculated currency field"""

    widget = CurrencyInput()

    def widget_attrs(self, widget: forms.Widget) -> dict[str, Any]:
        attrs = super().widget_attrs(widget)
        attrs.update({"class": attrs.get("class", "") + " calculated-currency-field"})
        return attrs


class ACFTextareaField(ACFFieldMixin, forms.CharField):
    """A text area field"""

    widget = forms.Textarea(attrs={"rows": 10, "cols": 70})


class ACFFileField(ACFFieldMixin, forms.FileField):
    """A file upload field with configurable allowed extensions and per-file size limit.

    TODO: Final allowed file types and maximum file size are pending confirmation from ACF.
    Provisional defaults: pdf, png, jpg, jpeg; 10 MB per file.
    """

    # Provisional defaults — pending final confirmation from ACF
    ALLOWED_EXTENSIONS = ["pdf", "png", "jpg", "jpeg"]
    MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

    def __init__(
        self,
        *args,
        allowed_extensions: list[str] | None = None,
        max_size_bytes: int | None = None,
        **kwargs,
    ):
        self.allowed_extensions = (
            allowed_extensions if allowed_extensions is not None else self.ALLOWED_EXTENSIONS
        )
        self.max_size_bytes = (
            max_size_bytes if max_size_bytes is not None else self.MAX_SIZE_BYTES
        )
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if value:
            filename = getattr(value, "name", "")
            if "." in filename:
                ext = filename.rsplit(".", 1)[-1].lower()
                if ext not in self.allowed_extensions:
                    allowed = ", ".join(self.allowed_extensions)
                    raise forms.ValidationError(
                        f"File type '.{ext}' is not allowed. Allowed types: {allowed}."
                    )
            size = getattr(value, "size", 0)
            if size > self.max_size_bytes:
                mb = self.max_size_bytes // (1024 * 1024)
                raise forms.ValidationError(f"File size must not exceed {mb} MB.")


class ACFBoundFieldFilterField(BoundField):

    def get_fields_to_exclude(self):
        """Return a list of field names that should be excluded based on the filter fields."""
        all_filterable_fields = []
        selected_fields = []

        for value in self.value() or []:
            selected_fields += value.split(",")

        field = cast(ACFFieldFilterField, self.field)

        choices = cast(Iterable, field.choices)

        for value, _ in choices:
            all_filterable_fields += value.split(",")

        # If no fields were selected for inclusion, exclude everything
        if not selected_fields:
            return all_filterable_fields

        # If some fields were selected, exclude the others that weren't selected
        return list(set(all_filterable_fields) - set(selected_fields))


class ACFBooleanField(ACFFieldMixin, forms.BooleanField):
    """A boolean field rendered via the c-checkbox design system component."""

    widget = ACFCheckboxInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.label = self.title or ""


class ACFFieldFilterField(ACFFieldMixin, forms.MultipleChoiceField):
    """A special field that defines fields to exclude from subsequent interview questions."""

    bound_field_class = ACFBoundFieldFilterField

    widget = CheckboxSelectMultiple


class ACFYesNoDisplayField(ACFFieldMixin, forms.MultiValueField):
    """A form field that asks a question and shows a radio button with yes and no choices,
    and conditionally displays a field based on the selection of yes or no."""

    widget = YesNoDisplayWidget

    error_messages = {}

    def __init__(self, fields, *args, require_all_fields=False, **kwargs):

        fields = [
            acf_fields.ChoiceField(
                choices=[
                    ("yes", "Yes"),
                    ("no", "No"),
                ],
                widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
                initial="no",
            ),
        ] + fields

        subwidgets = []

        for field in fields:

            field = cast(ACFField, field)

            field.widget.attrs.update(
                {
                    "label": field.title,
                }
            )
            subwidgets.append(field.widget)

        widget = self.widget(widgets=subwidgets)

        super().__init__(
            fields, *args, widget=widget, require_all_fields=require_all_fields, **kwargs
        )

    def compress(self, data_list):

        # To Do: we probably need to store these values some other way, like not with
        # a dash as a delimiter.
        return "-".join([str(d) for d in data_list])


class ACFFieldsMeta(type):

    def __new__(cls, name, bases=(), dct=None):
        """A metaclass that creates an object of custom ACF form fields from built-in Django
        form fields. They're all accessible on the acf_fields object below."""

        dct = dct or {}

        for name, field_class in forms.fields.__dict__.items():

            try:
                if not issubclass(field_class, forms.Field):
                    continue
            except TypeError:
                continue

            dct.update({name: type(name, (ACFFieldMixin, field_class), {})})

        dct.update(
            {
                "BooleanField": ACFBooleanField,
                "IntegerField": ACFIntegerField,
                "CurrencyField": ACFCurrencyField,
                "TextareaField": ACFTextareaField,
                "FileField": ACFFileField,
                "CalculatedCurrencyField": ACFCalculatedCurrencyField,
                "CalculatedIntegerField": ACFCalculatedIntegerField,
                "CalculatedDecimalField": ACFCalculatedDecimalField,
                "FieldFilterField": ACFFieldFilterField,
                "YesNoDisplayField": ACFYesNoDisplayField,
            }
        )

        return super().__new__(cls, name, bases, dct)


class acf_fields(metaclass=ACFFieldsMeta):

    ChoiceField: type[forms.ChoiceField]
