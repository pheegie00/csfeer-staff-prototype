import logging
from urllib.parse import parse_qs, urlencode, urlsplit

from django.http.request import HttpRequest
from django.views.generic import TemplateView
from oauth2_authcodeflow.views import CallbackView

logger = logging.getLogger(__name__)


class CoreAuthCallbackView(CallbackView):

    def append_error_params(self, request, url):
        login_error = None
        login_error_description = None
        login_error_source = None

        error_param = request.GET.get("error")

        if not error_param:
            url_parts = urlsplit(url)
            parsed_qs = parse_qs(url_parts.query)
            error_param = parsed_qs.get("error", [None])[0]

        match error_param:

            # An okta error from login.acf.gov will have
            # error=access_denied
            case "access_denied":
                login_error = "Access Denied"
                login_error_description = request.GET.get("error_description")
                login_error_source = "okta"

            # If there's an auth error from the app,
            # the library will return the user as None
            # and provide this error as the error query param
            case "OIDC authent callback, no user error":
                login_error = "Setup Incomplete"
                login_error_description = "Your account isn't set up yet."
                login_error_source = "app"

            case "_":
                login_error = None
                login_error_description = None
                login_error_source = None

        if login_error:

            url += "&" + urlencode(
                {
                    "login_error": login_error,
                    "login_error_description": login_error_description,
                    "login_error_source": login_error_source,
                }
            )

        return url

    def auth_callback(self, request, *args, **kwargs):
        url = super().auth_callback(request, *args, **kwargs)

        return self.append_error_params(request, url)

    def get_redirect_url(self, request: HttpRequest, *args, **kwargs) -> str:
        """Overloaded to append the error_description
        value that might be passed back by login.acf.gov
        if the login fails for some reason."""

        url = super().get_redirect_url(request, *args, **kwargs)
        return self.append_error_params(request, url)


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "login_error": self.request.GET.get("login_error"),
                "login_error_description": self.request.GET.get("login_error_description"),
                "login_error_source": self.request.GET.get("login_error_source"),
            }
        )

        return context
