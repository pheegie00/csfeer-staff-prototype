from users.models import CoreUser


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
    return user.has_perm("form_manager.form_start", organization)
