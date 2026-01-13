from django import forms


class CurrencyInput(forms.NumberInput):
    """Displays a currency input form field."""

    template_name = "form_manager/widgets/currency.html"


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """A multi-checkbox component."""

    template_name = "form_manager/widgets/checkbox_select_multiple.html"
