from dataclasses import field

from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields
from form_manager.schema.layout import (
    FieldBlock,
    PageBlock,
    PermanentPageBlock,
    SectionBlock,
    StepBlock,
)
from form_manager.views.form_edit import remove_nodes_with_excluded_fields


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
    """Ensure that fieldblocks and pageblocks are removed when fieldsblocks are children of pageblocks."""
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
    """Ensure that fieldblocks and pages are removed when the fieldblock is nested inside a component that's not a pageblock."""
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
