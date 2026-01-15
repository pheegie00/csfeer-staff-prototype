from typing import Any

from django import template

from form_manager.schema.layout import FieldBlock

register = template.Library()


"""
steps = [
    {
        "title": "",
        "edit_url": "",
        "fields": [
        
        ]
    },
    {
    
    }

]


"""


def flatten_for_review(initial_steps: list[Any]):

    final = []

    # The last item in the list of steps should be the review step,
    # and we don't need to render that, so remove it
    initial_steps.pop()

    for initial_step in initial_steps:

        step = {
            "title": initial_step.title,
            "edit_url": "",
            "fields": [],
        }

        # recurse down the tree and find all the FieldBlocks
        # and add them to the fields list

        def find_fields(node, fields: list[FieldBlock]):

            for child in node.children:

                if isinstance(child, FieldBlock):
                    fields.append(child)

                if child.children:

                    fields = find_fields(child, fields)

            return fields

        fields = find_fields(initial_step, [])

        step["fields"] = fields

        final.append(step)

    print(final)

    return final


register.filter("flatten_for_review", flatten_for_review)


# class CustomNode(template.Node):

#     def __init__(self, steps):
#         self.steps = template.Variable(steps)

#     def render(self, context):
#         print(context)
#         steps = self.steps.resolve(context)

#         print(steps)

#         return ""


# def render_review_page(parser, token):

#     _name, _var = token.split_contents()

#     return CustomNode(_var)


# register.tag("render_review_page", render_review_page)
