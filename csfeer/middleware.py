"""Custom middleware overrides for the CORE deployment.

LoginRequiredMiddlewareWithCurrentPath:
    The upstream oauth2_authcodeflow LoginRequiredMiddleware caches the
    `next` URL in the session every time the user authenticates and reuses
    it on the NEXT unauthenticated request, regardless of the URL the user
    actually visited. That means: a user whose previous session went
    through /forms/ keeps getting redirected back to /forms/ after every
    fresh login, even if they tried to open /staff/.

    Override: prefer the URL the user actually requested (request.path) over
    the cached session value. The cached value is still used as a last-
    resort fallback so existing behavior of explicit `?next=` params and
    session-stored values still works.
"""

from oauth2_authcodeflow.middleware import LoginRequiredMiddleware


class LoginRequiredMiddlewareWithCurrentPath(LoginRequiredMiddleware):
    """Send users back to the page they tried to load, not a stale cached URL."""

    def get_param_url(self, request, get_field, session_field):
        # 1. Honor explicit ?next= or ?fail= GET params (existing behavior).
        url = request.GET.get(get_field) if request.method == "GET" else None
        if url:
            return request.build_absolute_uri(url)

        # 2. Otherwise prefer the URL the user is currently requesting.
        # This is the key fix vs. upstream: upstream goes straight to
        # session cache here, which causes stale-next-URL bugs.
        # We only use request.path for the "next" field. The "fail" field
        # still uses the session cache so error redirects don't loop on
        # the same broken page.
        from oauth2_authcodeflow import constants
        if session_field == constants.SESSION_NEXT_URL:
            if request.path and request.path not in ("/oidc/", "/oidc/authenticate", "/oidc/callback"):
                return request.build_absolute_uri(request.path)

        # 3. Fall through to session cache, then "/".
        url = request.session.get(session_field) or "/"
        return request.build_absolute_uri(url)
