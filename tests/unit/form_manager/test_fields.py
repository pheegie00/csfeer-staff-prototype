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


def test_calculated_currency_field_ignores_initial_data():
    """Ensure the calculated currency field ignores its initial data value and always
    calculates a fresh value when instantiated."""

    class TestForm(BaseFields):

        item_1 = acf_fields.CurrencyField()
        item_2 = acf_fields.CurrencyField()
        item_3 = acf_fields.CurrencyField()
        total = acf_fields.CalculatedCurrencyField(fields=["item_1", "item_2", "item_3"])

    form = TestForm(
        initial={
            "item_1": 10,
            "item_2": 10,
            "item_3": 10,
            "total": 1000,
        }
    )

    form.is_valid()

    assert form["total"].value() == "30.00"

    form = TestForm(
        data={
            "item_1": 10,
            "item_2": 10,
            "item_3": 10,
            "total": 1000,
        },
    )

    assert form.is_valid()

    assert form.cleaned_data["total"] == 30.00


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


def test_field_filter_field_excludes_correct_fields(subtests):
    """Ensure the FieldFilterField works as expected."""

    class TestForm(BaseFields):

        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1,field2", "Topic 1"),
                ("field3", "Topic 2"),
                ("field4,field5", "Topic 3"),
            ],
        )

    test_data = [
        # nothing selected, all fields excluded
        ([], ["field1", "field2", "field3", "field4", "field5"]),
        # field1 and field2 are selected, 3, 4 and 5 are excluded
        (["field1,field2"], ["field3", "field4", "field5"]),
        # field3 is selected, 1, 2, 4 and 5 are excluded
        (["field3"], ["field1", "field2", "field4", "field5"]),
        # all fields selected, none are excluded
        (["field1,field2", "field3", "field4,field5"], []),
    ]

    for selected, expected_excluded in test_data:
        with subtests.test(selected=selected, expected_excluded=expected_excluded):
            form = TestForm(
                data={
                    "topics": selected,
                }
            )

            form.is_valid()

            assert set(form.fields_to_exclude) - set(expected_excluded) == set()
