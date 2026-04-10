from typing import Any

from django import template

from form_manager.schema.fields import _StorageFilePath
from form_manager.schema.layout import FieldBlock, ReviewSubheadingBlock

register = template.Library()


@register.filter
def as_file_list(value) -> list[_StorageFilePath]:
    """Convert a stored file value (string or list of strings) to a list of _StorageFilePath
    objects suitable for rendering links in review templates."""
    if not value:
        return []
    if isinstance(value, str):
        return [_StorageFilePath(value)]
    if isinstance(value, list):
        return [_StorageFilePath(v) for v in value if v]
    return []


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
