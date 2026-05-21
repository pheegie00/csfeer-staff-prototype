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

StaleCallbackRedirectMiddleware:
    The OIDC callback view requires SESSION_NEXT_URL and SESSION_FAIL_URL
    to be set in the session (they're set during the prior /oidc/authenticate
    redirect). If a user reloads a stale /oidc/callback?code=... URL after
    logging out, the upstream view returns 400 ('session parameters should
    be filled'). Bounce them to /staff/ instead so they restart the flow
    cleanly with no visible error.
"""

from django.http import HttpResponseRedirect
from oauth2_authcodeflow import constants
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


class StaleCallbackRedirectMiddleware:
    """Bounce stale /oidc/callback hits to /staff/ instead of 400'ing.

    Happens when a user reloads a browser tab that was at /oidc/callback
    after their session was logged out. The OIDC code is replayed but
    the session is empty, so the upstream callback view returns 400.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/oidc/callback":
            has_next = request.session.get(constants.SESSION_NEXT_URL)
            has_fail = request.session.get(constants.SESSION_FAIL_URL)
            if not has_next or not has_fail:
                # Session lost the next/fail state. Restart the flow from /staff/.
                return HttpResponseRedirect("/staff/")
        return self.get_response(request)
