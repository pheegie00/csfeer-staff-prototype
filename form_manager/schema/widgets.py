from django import forms


class CurrencyInput(forms.NumberInput):
    template_name = "form_manager/widgets/currency.html"
