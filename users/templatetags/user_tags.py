import django.template as template

from users.utils import (
    user_can_edit,
    user_can_list_forms,
    user_can_start_form,
    user_can_submit,
    user_can_view,
    user_is_authorized_official,
)

register = template.Library()


@register.simple_tag
def can_submit_form(user, organization):
    return user_can_submit(user, organization)


@register.simple_tag
def can_view_form(user, organization):
    return user_can_view(user, organization)


@register.simple_tag
def can_edit_form(user, organization):
    return user_can_edit(user, organization)


@register.simple_tag
def can_list_forms(user, organization):
    return user_can_list_forms(user, organization)


@register.simple_tag
def can_start_form(user, organization):
    return user_can_start_form(user, organization)


@register.simple_tag
def is_authorized_official(user, organization):
    return user_is_authorized_official(user, organization)
