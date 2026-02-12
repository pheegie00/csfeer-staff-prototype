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
        ("", ""),
        (None, ""),
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


def test_yesno_display_field():

    class TestForm(BaseFields):

        spent = acf_fields.YesNoDisplayField(
            title="Did you spend any money?",
            fields=[acf_fields.CurrencyField(title="Enter the amount spent")],
        )

    data = {
        "spent_0": "yes",
        "spent_1": "10.00",
    }

    form = TestForm(data)

    assert form.is_valid()

    assert form.cleaned_data["spent"] == "-".join(data.values())

    assert form["spent"].value() == list(data.values())


def test_yesno_display_field_as_list():

    class TestForm(BaseFields):

        spent = acf_fields.YesNoDisplayField(
            title="Did you spend any money?",
            fields=[acf_fields.CurrencyField(title="Enter the amount spent")],
        )

    data = {
        "spent": ["yes", "10.00"],
    }

    form = TestForm(data)

    assert form.is_valid()

    assert form.cleaned_data["spent"] == "-".join(data["spent"])

    assert form["spent"].value() == data["spent"]


def test_excluded_required_field_uses_default_with_use_default_if_empty():
    """When required field with default_if_excluded is excluded and use_default_if_empty=True, use default."""
    from decimal import Decimal

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
                ("field2", "Topic 2"),
            ],
        )
        field1 = acf_fields.CurrencyField(title="Field 1", required=True, default_if_excluded=0)
        field2 = acf_fields.CharField(title="Field 2", required=True, default_if_excluded="N/A")

    # Select only field1, so field2 is excluded
    form = TestForm(data={"topics": ["field1"], "field1": "100"})

    # With use_default_if_empty=True, excluded field should use default
    assert form.is_valid(use_default_if_excluded=True), f"Form errors: {form.errors}"
    assert form.cleaned_data["field1"] == Decimal("100")
    assert form.cleaned_data["field2"] == "N/A"  # Should use default


def test_excluded_required_field_fails_without_use_default_if_empty():
    """When required field with default_if_excluded is excluded but use_default_if_empty=False, fail validation."""

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
                ("field2", "Topic 2"),
            ],
        )
        field1 = acf_fields.CurrencyField(title="Field 1", required=True, default_if_excluded=0)
        field2 = acf_fields.CharField(title="Field 2", required=True, default_if_excluded="N/A")

    # Select only field1, so field2 is excluded
    form = TestForm(data={"topics": ["field1"], "field1": "100"})

    # Without use_default_if_empty=True, excluded required field should fail
    assert not form.is_valid()
    assert "field2" in form.errors


def test_excluded_field_user_can_override_when_not_excluded():
    """When field is not excluded, user input takes precedence."""
    from decimal import Decimal

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
                ("field2", "Topic 2"),
            ],
        )
        field1 = acf_fields.CurrencyField(title="Field 1", required=True, default_if_excluded=0)
        field2 = acf_fields.CharField(title="Field 2", required=True, default_if_excluded="N/A")

    # Select both fields
    form = TestForm(data={"topics": ["field1", "field2"], "field1": "100", "field2": "User Input"})

    assert form.is_valid(use_default_if_excluded=True), f"Form errors: {form.errors}"
    assert form.cleaned_data["field1"] == Decimal("100")
    assert form.cleaned_data["field2"] == "User Input"  # User input, not default


def test_required_field_without_default_if_excluded_fails_when_excluded():
    """Without default_if_excluded, excluded required field should fail validation even with use_default_if_empty=True."""

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
                ("field2", "Topic 2"),
            ],
        )
        field1 = acf_fields.CurrencyField(title="Field 1", required=True)
        field2 = acf_fields.CharField(title="Field 2", required=True, default_if_excluded="N/A")

    # Select only field2, field1 is excluded but has no default_if_excluded
    form = TestForm(data={"topics": ["field2"], "field2": "Value"})

    # Form should be invalid because field1 is required but has no default
    assert not form.is_valid(use_default_if_excluded=True)
    assert "field1" in form.errors


def test_optional_field_with_default_if_excluded():
    """Optional field with default_if_excluded uses default when excluded and use_default_if_empty=True."""

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
                ("field2", "Topic 2"),
            ],
        )
        field1 = acf_fields.CharField(title="Field 1", required=True)
        field2 = acf_fields.CharField(
            title="Field 2", required=False, default_if_excluded="Optional Default"
        )

    # Select only field1, field2 is excluded
    form = TestForm(data={"topics": ["field1"], "field1": "Value"})

    assert form.is_valid(use_default_if_excluded=True), f"Form errors: {form.errors}"
    assert form.cleaned_data["field1"] == "Value"
    assert form.cleaned_data["field2"] == "Optional Default"


def test_default_if_excluded_with_different_field_types():
    """Test default_if_excluded with different field types when use_default_if_empty=True."""
    from decimal import Decimal

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("selected", "Selected Topic"),
                ("currency_field,char_field,integer_field", "Other Fields"),
            ],
        )
        selected = acf_fields.CharField(title="Selected", required=True)
        currency_field = acf_fields.CurrencyField(
            title="Currency", required=True, default_if_excluded="0.00"
        )
        char_field = acf_fields.CharField(
            title="Char", required=True, default_if_excluded="Default Text"
        )
        integer_field = acf_fields.IntegerField(
            title="Integer", required=True, default_if_excluded="0"
        )

    # Select only "selected" topic, so other fields are excluded
    form = TestForm(
        data={
            "topics": ["selected"],
            "selected": "Value",
        }
    )

    assert form.is_valid(use_default_if_excluded=True)
    assert form.cleaned_data["selected"] == "Value"
    assert form.cleaned_data["currency_field"] == Decimal("0.00")
    assert form.cleaned_data["char_field"] == "Default Text"
    assert form.cleaned_data["integer_field"] == 0


def test_default_if_excluded_none_behaves_normally():
    """Field with default_if_excluded=None should behave like normal field."""

    class TestForm(BaseFields):
        topics = acf_fields.FieldFilterField(
            choices=[
                ("field1", "Topic 1"),
            ],
        )
        field1 = acf_fields.CharField(title="Field 1", required=True)
        field2 = acf_fields.CharField(title="Field 2", required=True, default_if_excluded=None)

    # Select only field1, field2 is excluded
    form = TestForm(data={"topics": ["field1"], "field1": "Value"})

    # Form should be invalid because field2 is required and has no default
    assert not form.is_valid(use_default_if_excluded=True)
    assert "field2" in form.errors
