from django import forms

from .widgets import CalculatedCurrencyInput, CalculatedField, CurrencyInput

FIELD_TEMPLATE_NAME = "form_manager/forms/field.html"


def generate_django_form_field_from_schema(
    name: str, field: dict[str, str | bool], required: bool
) -> forms.CharField | forms.EmailField | forms.FloatField | None:
    """Generates a django form field from a JSON schema field definition."""
    label = field.get("title", name)
    help_text = field.get("description", "")
    max_length = field.get("maxLength")
    min_length = field.get("minLength")
    field_type = field.get("fieldType", None)
    derrived_fields = field.get("fields", None)
    field_object = None

    if field_type == "TextField":
        field_object = forms.CharField(
            label=label,
            required=required,
            help_text=help_text,
            max_length=max_length,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )
    elif field_type == "EmailField":
        field_object = forms.EmailField(
            label=label,
            required=required,
            help_text=help_text,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )
    elif field_type == "PhoneNumberField":
        field_object = forms.CharField(
            label=label,
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )
    elif field_type == "CurrencyField":
        field_object = forms.FloatField(
            label=label,
            required=required,
            help_text=help_text,
            widget=CurrencyInput,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )
    elif field_type == "CalculatedCurrencyField":
        field_object = CalculatedField(
            label=label,
            required=required,
            help_text=help_text,
            widget=CalculatedCurrencyInput,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
            derrived_field_names=derrived_fields,
        )
    elif field_type == "TextareaField":
        field_object = forms.CharField(
            label=label,
            required=required,
            help_text=help_text,
            widget=forms.Textarea,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )
    elif field_type == "ComputedField":
        field_object = forms.CharField(
            label=label,
            required=required,
            help_text=help_text,
            disabled=True,
            widget=CalculatedCurrencyInput,
            template_name=FIELD_TEMPLATE_NAME,  # pyright: ignore
        )

    return field_object
