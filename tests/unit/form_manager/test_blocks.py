from form_manager.schema.layout import (
    CardBlock,
    ConditionalBlock,
    FieldBlock,
    PageBlock,
    PermanentPageBlock,
    SectionBlock,
    StepBlock,
)
from form_manager.schema.navigation import remove_nodes_with_excluded_fields


class _StubBoundField:
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value


class _StubForm:
    """Minimal stand-in for a Django form — only indexes fields by name."""

    def __init__(self, values: dict):
        self._values = values

    def __getitem__(self, name):
        if name not in self._values:
            raise KeyError(name)
        return _StubBoundField(self._values[name])


def test_has_field_blocks():
    """Ensure the StepBlock.has_field_blocks method works."""

    from form_manager.schema.layout import (
        FieldBlock,
        PageBlock,
        SectionBlock,
        StepBlock,
    )

    step_with_fields = StepBlock(
        children=[
            PageBlock(
                children=[
                    SectionBlock(
                        children=[
                            FieldBlock(field_name="field1"),
                        ]
                    )
                ]
            )
        ]
    )

    step_without_fields = StepBlock(children=[PageBlock(children=[SectionBlock(children=[])])])

    assert StepBlock.has_field_blocks(step_with_fields) is True
    assert StepBlock.has_field_blocks(step_without_fields) is False


def test_conditional_filter():
    """Ensure page blocks are removed when excluded field blocks are their children."""
    components = [
        StepBlock(
            children=[
                PageBlock(children=[FieldBlock(field_name="field1")]),
                PageBlock(children=[FieldBlock(field_name="field2")]),
            ]
        ),
        StepBlock(
            children=[
                PageBlock(children=[FieldBlock(field_name="field3")]),
                PageBlock(children=[FieldBlock(field_name="field4")]),
            ]
        ),
    ]

    result = remove_nodes_with_excluded_fields(components, ["field1"])
    assert result
    assert result[0].children and len(result[0].children) == 1
    assert result[1].children and len(result[1].children) == 2


def test_conditional_filter_nested_fieldblock():
    """Ensure nested excluded field blocks still cause empty pages to be removed."""
    components = [
        StepBlock(
            children=[
                PageBlock(children=[FieldBlock(field_name="field1")]),
                PageBlock(children=[FieldBlock(field_name="field2")]),
            ]
        ),
        StepBlock(
            children=[
                PageBlock(children=[FieldBlock(field_name="field3")]),
                PageBlock(
                    children=[
                        SectionBlock(children=[FieldBlock(field_name="field4")]),
                    ]
                ),
            ]
        ),
    ]

    result = remove_nodes_with_excluded_fields(components, ["field4"])
    assert result[0].children and len(result[0].children) == 2
    assert result[1].children and len(result[1].children) == 1


def test_conditional_filter_permanent_pageblock():
    """Ensure that PermanentPageBlock nodes aren't removed if their fields are removed"""
    components = [
        StepBlock(
            children=[
                PermanentPageBlock(children=[FieldBlock(field_name="field1")]),
                PageBlock(children=[FieldBlock(field_name="field2")]),
            ]
        ),
        StepBlock(
            children=[
                PageBlock(children=[FieldBlock(field_name="field3")]),
                PageBlock(
                    children=[
                        SectionBlock(children=[FieldBlock(field_name="field4")]),
                    ]
                ),
            ]
        ),
    ]

    result = remove_nodes_with_excluded_fields(components, ["field1"])
    assert len(result) == 2
    assert result[0].children and result[0].children.__len__() == 2
    assert result[1].children and result[1].children.__len__() == 2


def test_conditional_filter_keeps_empty_steps_for_side_nav():
    """Ensure fully excluded steps remain present so the side nav can disable them."""
    components = [
        StepBlock(children=[PageBlock(children=[FieldBlock(field_name="field1")])]),
        StepBlock(children=[PageBlock(children=[FieldBlock(field_name="field2")])]),
    ]

    result = remove_nodes_with_excluded_fields(components, ["field2"])

    assert len(result) == 2
    assert result[0].children and len(result[0].children) == 1
    assert result[1].children == []


def test_conditional_block_title_defaults_to_none():
    """ConditionalBlock should not require a title."""
    block = ConditionalBlock(
        show_when="yes",
        children=[FieldBlock(field_name="field1")],
    )

    assert block.title is None


def test_conditional_block_accepts_title():
    """ConditionalBlock should accept an optional title for inline rendering."""
    block = ConditionalBlock(
        title="Additional Authorized Official",
        show_when="yes",
        children=[FieldBlock(field_name="field1")],
    )

    assert block.title == "Additional Authorized Official"


def test_conditional_block_renders_title_when_present():
    """When a title is set the rendered template should include an h2 heading."""
    block = ConditionalBlock(
        title="Additional Authorized Official",
        show_when="yes",
        children=[],
    )

    rendered = str(block.render())

    assert "Additional Authorized Official" in rendered
    assert "<h2" in rendered


def test_conditional_block_omits_heading_when_no_title():
    """Without a title the rendered template should not include an h2 heading."""
    block = ConditionalBlock(
        show_when="yes",
        children=[],
    )

    rendered = str(block.render())

    assert "<h2" not in rendered


def test_conditional_block_show_when_expression_single_value():
    """show_when_expression should render a single string as a one-element list."""
    block = ConditionalBlock(show_when="yes", children=[])

    assert block.show_when_expression == "['yes'].includes(checked)"


def test_conditional_block_show_when_expression_list_values():
    """show_when_expression should render a list of strings as a multi-element list."""
    block = ConditionalBlock(show_when=["one_year", "two_year"], children=[])

    assert block.show_when_expression == "['one_year', 'two_year'].includes(checked)"


def test_card_block_should_render_without_show_when_field():
    """A CardBlock with no show_when_field renders unconditionally."""
    block = CardBlock(title="Year one", children=[])

    assert block.should_render is True


def test_card_block_should_render_when_form_missing():
    """Without an attached form (e.g. raw schema rendering) the card renders."""
    block = CardBlock(show_when_field="plan_coverage", show_when_value="one_year", children=[])

    assert block.should_render is True


def test_card_block_should_render_when_field_missing_from_form():
    """If the controlling field isn't on the form, fall back to rendering."""
    block = CardBlock(show_when_field="missing_field", show_when_value="x", children=[])
    block.set_extra_context(form=_StubForm({}))

    assert block.should_render is True


def test_card_block_should_render_when_value_matches_string():
    """Card renders when the form value equals the single show_when_value."""
    block = CardBlock(show_when_field="plan_coverage", show_when_value="two_year", children=[])
    block.set_extra_context(form=_StubForm({"plan_coverage": "two_year"}))

    assert block.should_render is True


def test_card_block_should_not_render_when_value_does_not_match_string():
    """Card is hidden when the form value doesn't match show_when_value."""
    block = CardBlock(show_when_field="plan_coverage", show_when_value="two_year", children=[])
    block.set_extra_context(form=_StubForm({"plan_coverage": "one_year"}))

    assert block.should_render is False


def test_card_block_should_render_when_value_matches_any_in_list():
    """Card renders when the form value matches any entry in a list show_when_value."""
    block = CardBlock(
        show_when_field="plan_coverage",
        show_when_value=["one_year", "two_year"],
        children=[],
    )
    block.set_extra_context(form=_StubForm({"plan_coverage": "one_year"}))

    assert block.should_render is True


def test_card_block_should_not_render_when_value_missing_from_list():
    """Card is hidden when the form value isn't in the list of allowed values."""
    block = CardBlock(
        show_when_field="plan_coverage",
        show_when_value=["one_year", "two_year"],
        children=[],
    )
    block.set_extra_context(form=_StubForm({"plan_coverage": None}))

    assert block.should_render is False


def test_card_block_should_render_on_truthy_value_without_show_when_value():
    """When show_when_value is None, the card uses truthiness of the form value."""
    block = CardBlock(show_when_field="plan_coverage", children=[])
    block.set_extra_context(form=_StubForm({"plan_coverage": "one_year"}))

    assert block.should_render is True


def test_card_block_should_not_render_on_falsy_value_without_show_when_value():
    """When show_when_value is None and the form value is falsy, the card is hidden."""
    block = CardBlock(show_when_field="plan_coverage", children=[])
    block.set_extra_context(form=_StubForm({"plan_coverage": ""}))

    assert block.should_render is False
