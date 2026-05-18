import logging

import pytest
from oauth2_authcodeflow.auth import AuthenticationBackend
from unittest.mock import MagicMock, patch


@pytest.fixture
def backend():
    from csfeer.auth_backends.oidc_backend import EmailOIDCAuthenticationBackend

    return EmailOIDCAuthenticationBackend()


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        email="test@example.com",
        password="testpassword",
        first_name="",
        last_name="",
    )


CLAIMS = {"given_name": "Alice", "family_name": "Smith"}
REQUEST = MagicMock()
ACCESS_TOKEN = "token"

OIDC_SETTINGS = {
    "OIDC_FIRSTNAME_CLAIM": "given_name",
    "OIDC_LASTNAME_CLAIM": "family_name",
    "OIDC_UNUSABLE_PASSWORD": False,
    "OIDC_EXTEND_USER": None,
}


class TestNamePreservation:
    def test_names_populated_from_claims_when_blank(self, backend, user):
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.first_name == "Alice"
        assert user.last_name == "Smith"

    def test_existing_first_name_not_overwritten(self, backend, user):
        user.first_name = "Existing"
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.first_name == "Existing"

    def test_existing_last_name_not_overwritten(self, backend, user):
        user.last_name = "Existing"
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.last_name == "Existing"

    def test_callable_firstname_claim(self, backend, user):
        settings = {**OIDC_SETTINGS, "OIDC_FIRSTNAME_CLAIM": lambda c: "Callable"}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.first_name == "Callable"

    def test_callable_lastname_claim(self, backend, user):
        settings = {**OIDC_SETTINGS, "OIDC_LASTNAME_CLAIM": lambda c: "Callable"}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.last_name == "Callable"

    def test_missing_claim_key_falls_back_to_empty_string(self, backend, user):
        settings = {**OIDC_SETTINGS, "OIDC_FIRSTNAME_CLAIM": "nonexistent_key"}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert user.first_name == ""


# ---------------------------------------------------------------------------
# Password handling
# ---------------------------------------------------------------------------


class TestPasswordHandling:
    def test_unusable_password_set_for_new_user(self, backend, user):
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(
                user, created=True, claims=CLAIMS, request=REQUEST, access_token=ACCESS_TOKEN
            )

        assert not user.has_usable_password()

    def test_unusable_password_not_set_for_existing_user_by_default(self, backend, user):
        user.set_password("secret")
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(
                user, created=False, claims=CLAIMS, request=REQUEST, access_token=ACCESS_TOKEN
            )

        assert user.has_usable_password()

    def test_unusable_password_forced_by_setting(self, backend, user):
        user.set_password("secret")
        settings = {**OIDC_SETTINGS, "OIDC_UNUSABLE_PASSWORD": True}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(
                user, created=False, claims=CLAIMS, request=REQUEST, access_token=ACCESS_TOKEN
            )

        assert not user.has_usable_password()


class TestExtendUser:
    def test_extend_user_called_with_two_args(self, backend, user):
        extend = MagicMock()
        settings = {**OIDC_SETTINGS, "OIDC_EXTEND_USER": extend}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        extend.assert_called_once_with(user, CLAIMS)

    def test_extend_user_called_with_four_args_when_signature_supports_it(self, backend, user):
        calls = []

        def extend_func(u, c, r, t):
            calls.append((u, c, r, t))

        settings = {**OIDC_SETTINGS, "OIDC_EXTEND_USER": extend_func}
        with patch("csfeer.auth_backends.oidc_backend.settings", **settings):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert calls == [(user, CLAIMS, REQUEST, ACCESS_TOKEN)]

    def test_extend_user_not_called_when_none(self, backend, user):
        called = []
        with patch("csfeer.auth_backends.oidc_backend.settings", **OIDC_SETTINGS):
            backend.update_user(user, False, CLAIMS, REQUEST, ACCESS_TOKEN)

        assert called == []


class EmailOIDCAuthenticationBackend:

    def _get_mock_user_model(self, mock_user, created=False):
        mock_model = MagicMock()
        mock_model.objects.get_or_create.return_value = (mock_user, created)
        return mock_model

    def test_update_user_called_with_correct_args(self, backend):
        mock_user = MagicMock()
        with (
            patch.object(
                backend, "get_full_claims", return_value={"email": "test@example.com", **CLAIMS}
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.settings",
                OIDC_SETTINGS
                | {
                    "OIDC_OP_EXPECTED_EMAIL_CLAIM": "email",
                    "OIDC_EMAIL_CLAIM": None,
                },
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.get_user_model",
                return_value=self._get_mock_user_model(mock_user, created=False),
            ),
            patch.object(backend, "update_user") as mock_update,
        ):
            backend.get_or_create_user(REQUEST, {}, ACCESS_TOKEN)

        mock_update.assert_called_once_with(
            mock_user, False, {"email": "test@example.com", **CLAIMS}, REQUEST, ACCESS_TOKEN
        )

    def test_user_save_called_after_update_user(self, backend):
        mock_user = MagicMock()
        with (
            patch.object(
                backend, "get_full_claims", return_value={"email": "test@example.com", **CLAIMS}
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.settings",
                OIDC_SETTINGS
                | {
                    "OIDC_OP_EXPECTED_EMAIL_CLAIM": "email",
                    "OIDC_EMAIL_CLAIM": None,
                },
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.get_user_model",
                return_value=self._get_mock_user_model(mock_user),
            ),
            patch.object(backend, "update_user"),
        ):
            backend.get_or_create_user(REQUEST, {}, ACCESS_TOKEN)

        mock_user.save.assert_called_once()

    def test_returns_user_from_get_or_create(self, backend):
        mock_user = MagicMock()
        with (
            patch.object(
                backend, "get_full_claims", return_value={"email": "test@example.com", **CLAIMS}
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.settings",
                OIDC_SETTINGS
                | {
                    "OIDC_OP_EXPECTED_EMAIL_CLAIM": "email",
                    "OIDC_EMAIL_CLAIM": None,
                },
            ),
            patch(
                "csfeer.auth_backends.oidc_backend.get_user_model",
                return_value=self._get_mock_user_model(mock_user),
            ),
            patch.object(backend, "update_user"),
        ):
            result = backend.get_or_create_user(REQUEST, {}, ACCESS_TOKEN)

        assert result == mock_user

    def test_returns_none_when_super_returns_none(self, backend):
        """Ensure authenticate_oauth2 eturns None when there's no user."""
        with patch.object(AuthenticationBackend, "authenticate_oauth2", return_value=None):
            result = backend.authenticate_oauth2()

        assert result is None

    def test_returns_none_and_logs_warning_when_no_org_membership(self, backend, caplog):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.org_memberships.exists.return_value = False

        with (
            patch.object(AuthenticationBackend, "authenticate_oauth2", return_value=mock_user),
            caplog.at_level(logging.WARNING, logger="csfeer.auth_backends.oidc_backend"),
        ):
            result = backend.authenticate_oauth2()

        assert result is None
        assert "not assigned to any organization" in caplog.text

    def test_returns_user_when_org_membership_exists(self, backend):
        mock_user = MagicMock()
        mock_user.org_memberships.exists.return_value = True

        with patch.object(AuthenticationBackend, "authenticate_oauth2", return_value=mock_user):
            result = backend.authenticate_oauth2()

        assert result == mock_user
