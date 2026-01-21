from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import (
    BaseFields,
)


def test_calculated_currency_field_form_valid():
    """Ensure the calculated currency field works as expected with a valid form."""

    class TestForm(BaseFields):

        item_1 = acf_fields.CurrencyField()
        item_2 = acf_fields.CurrencyField()
        item_3 = acf_fields.CurrencyField()
        total = acf_fields.CalculatedCurrencyField(fields=["item_1", "item_2", "item_3"])

    form = TestForm(data={"item_1": 1, "item_2": 2, "item_3": 3})

    assert form.is_valid()

    assert form.cleaned_data["total"] == 6.0


def test_calculated_currency_field_form_invalid():
    """Ensure the calculated currency field works as expected with an invalid form."""

    class TestForm(BaseFields):

        item_1 = acf_fields.CurrencyField()
        item_2 = acf_fields.CurrencyField()
        item_3 = acf_fields.CurrencyField()
        total = acf_fields.CalculatedCurrencyField(fields=["item_1", "item_2", "item_3"])

    form = TestForm(
        data={
            "item_1": 10,
            "item_2": 10,
        }
    )

    assert form.is_valid() is False

    assert form.cleaned_data["total"] == 20.0
    assert form["total"].value() == "20.00"


def test_currency_fields_are_properly_formatted():
    """Ensure the currency field correctly formats its value"""

    class TestForm(BaseFields):
        money = acf_fields.CurrencyField()

    test_data = [
        (30.00, "30.00"),
        (30.0, "30.00"),
        (30, "30.00"),
        ("30", "30.00"),
        ("", "0.00"),
        (None, "0.00"),
    ]

    for input_value, expected in test_data:
        form = TestForm(data={"money": input_value})
        assert form["money"].value() == expected
