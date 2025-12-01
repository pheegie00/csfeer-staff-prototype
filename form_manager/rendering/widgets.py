from numbers import Number

from django.forms import NumberInput


class CurrencyInput(NumberInput):
    """Special type of number input."""

    pass


class CalculatedInput(NumberInput):
    """Special input whose value should be the sum of certain other fields."""

    pass


class CalculatedCurrencyInput(NumberInput):
    """Special currency input whose value should be the sum of certain other fields."""

    pass
