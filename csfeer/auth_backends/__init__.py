from .form_permissions import FormPermissionBackend
from .oidc_backend import EmailOIDCAuthenticationBackend


def extend_user_with_roles(*args, **kwargs):
    """A proxy function to properly allow settings.OIDC_EXTEND_USER to parse the dotted path"""
    return EmailOIDCAuthenticationBackend.extend_user_with_roles(*args, **kwargs)


__ALL__ = ["EmailOIDCAuthenticationBackend", FormPermissionBackend]
