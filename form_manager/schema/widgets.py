from django import forms


class CurrencyInput(forms.NumberInput):
    """Displays a currency input form field."""

    template_name = "form_manager/widgets/currency.html"


class ACFCheckboxInput(forms.CheckboxInput):
    """A single checkbox rendered via the c-checkbox design system component."""

    template_name = "form_manager/widgets/checkbox.html"

    def __init__(self, *args, **kwargs):
        self.label = kwargs.pop("label", "")
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["label"] = self.label
        return context


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """A multi-checkbox component."""

    input_type = "checkbox_multiple"
    template_name = "form_manager/widgets/checkbox_select_multiple.html"


class YesNoDisplayWidget(forms.MultiWidget):

    template_name = "form_manager/widgets/yes_no_display.html"

    def decompress(self, value):
        """This splits the single value into separate subwidget values."""

        # To Do: we probably need to store these values some other way, like not with
        # a dash as a delimiter.

        if value:
            return value.split("-")

        return "", ""

    def value_from_datadict(self, data, files, name):

        if name in data:
            return data.get(name, [])

        return super().value_from_datadict(data, files, name)
