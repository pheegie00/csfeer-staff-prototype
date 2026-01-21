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
