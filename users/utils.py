from typing import TYPE_CHECKING

from users.models import CoreUser
from users.permissions import (
    FORM_EDIT,
    FORM_LIST,
    FORM_START,
    FORM_SUBMIT,
    FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    FORM_VIEW,
)

if TYPE_CHECKING:
    from form_manager.schema.layout import AbstractPageBlock


def user_can_submit(user: CoreUser, organization):
    return user.has_perm(f"form_manager.{FORM_SUBMIT}", organization)


def user_can_view(user: CoreUser, organization):
    return user.has_perm(f"form_manager.{FORM_VIEW}", organization)


def user_can_edit(user: CoreUser, organization):
    return user.has_perm(f"form_manager.{FORM_EDIT}", organization)


def user_can_list_forms(user: CoreUser, organization):
    return user.has_perm(f"form_manager.{FORM_LIST}", organization)


def user_can_start_form(user: CoreUser, organization):
    return user.has_perm(f"form_manager.{FORM_START}", organization)


def user_is_authorized_official(user: CoreUser, organization):
    return user.has_perm(
        f"form_manager.{FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL}", organization
    )


def user_meets_page_permissions(user: CoreUser, organization, page: "AbstractPageBlock") -> bool:
    return all(user.has_perm(perm, organization) for perm in page.submit_permissions)
