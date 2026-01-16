from typing import Any

from django import template

from form_manager.schema.layout import FieldBlock, ReviewSubheadingBlock

register = template.Library()


def flatten_for_review(initial_steps: list[Any]):
    """This is a template filter that takes a list of UI components and
    reduces it to a list of steps, each containing a list of FieldBlocks
    and ReviewSubheadingBlocks only, for rendering on the review page."""

    final = []

    for initial_step in initial_steps:

        step = {
            "title": initial_step.title,
            "edit_url": "",
            "blocks": [],
        }

        # recurse down the tree and find all the FieldBlocks
        # and add them to the fields list

        def find_review_blocks(node, fields: list[FieldBlock | ReviewSubheadingBlock]):

            for child in node.children:

                if isinstance(child, ReviewSubheadingBlock):
                    fields.append(child)

                if isinstance(child, FieldBlock):
                    fields.append(child)

                if child.children:

                    fields = find_review_blocks(child, fields)

            return fields

        fields = find_review_blocks(initial_step, [])

        step["blocks"] = fields

        final.append(step)

    return final


register.filter("flatten_for_review", flatten_for_review)
