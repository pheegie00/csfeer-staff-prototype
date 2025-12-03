from typing import Any

from django import forms
from django.forms import NumberInput


class CurrencyInput(NumberInput):
    """Special type of number input."""

    pass


class CalculatedInput(forms.NumberInput):
    """Special input whose value should be the sum of certain other fields."""

    pass


class CalculatedField(forms.FloatField):

    def __init__(self, *args, derrived_field_names=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.derrived_field_names = derrived_field_names

        self.bound_field_class = CalculatedBoundField


class CalculatedBoundField(forms.BoundField):
    """A special form field for calculating a value based on other form fields."""

    field: Any
    form: forms.BaseForm

    @property
    def data(self):
        """
        Return the data for this BoundField, or None if it wasn't given.
        """
        vals = []

        for field_name in self.field.derrived_field_names:
            other_field = self.form.fields.get(field_name)
            other_bound_field = self.form[field_name]

            if not other_field or not other_bound_field:
                continue

            other_field_value = other_field.widget.value_from_datadict(
                self.form.data, self.form.files, other_bound_field.html_name  # type: ignore
            )

            try:
                vals.append(float(other_field_value))
            except ValueError:
                pass

        return sum(vals)


class CalculatedCurrencyInput(forms.NumberInput):
    """Special currency input whose value should be the sum of certain other fields."""

    pass
