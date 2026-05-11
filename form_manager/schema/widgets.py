from django import forms


class CurrencyInput(forms.NumberInput):
    """Displays a currency input form field."""

    template_name = "form_manager/widgets/currency.html"


class PercentageInput(forms.NumberInput):
    """Displays a percentage input form field with a `%` suffix."""

    template_name = "form_manager/widgets/percentage.html"


class PhoneInput(forms.TextInput):
    """Telephone input that renders the USWDS masked input with an Alpine
    ``x-mask`` directive enforcing ``XXX-XXX-XXXX`` typing, and submits digits
    only to the server."""

    input_type = "tel"
    template_name = "form_manager/widgets/phone.html"

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if isinstance(value, str):
            return value.replace("-", "")
        return value


class DatePickerInput(forms.DateInput):
    """A USWDS-enhanced date picker. Renders a text input wrapped in a
    `.usa-date-picker` div; the bundled USWDS JS progressively enhances it
    with the mm/dd/yyyy placeholder, calendar icon, and date-picking calendar."""

    template_name = "form_manager/widgets/date_picker.html"
    input_type = "text"

    def __init__(self, attrs=None, format="%Y-%m-%d"):
        super().__init__(attrs=attrs, format=format)


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
