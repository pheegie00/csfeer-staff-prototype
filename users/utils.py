from typing import TYPE_CHECKING

from users.models import CoreUser

if TYPE_CHECKING:
    from form_manager.schema.layout import AbstractPageBlock


def user_can_submit(user: CoreUser, organization):
    return user.has_perm("form_manager.form_submit", organization)


def user_can_view(user: CoreUser, organization):
    return user.has_perm("form_manager.form_view", organization)


def user_can_edit(user: CoreUser, organization):
    return user.has_perm("form_manager.form_edit", organization)


def user_can_list_forms(user: CoreUser, organization):
    return user.has_perm("form_manager.form_list", organization)


def user_can_start_form(user: CoreUser, organization):
    return user.has_perm("form_manager.form_start", organization)


def user_is_authorized_official(user: CoreUser, organization):
    return user.has_perm("form_manager.form_tribal_plan_can_sign_authorized_official", organization)


def user_meets_page_permissions(user: CoreUser, organization, page: "AbstractPageBlock") -> bool:
    return all(user.has_perm(perm, organization) for perm in page.submit_permissions)
