"""
URL configuration for csfeer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.apps import apps
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from form_manager.api import api as form_api

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path(
        "login-error/", TemplateView.as_view(template_name="login_error.html"), name="login_error"
    ),
    path("admin/", admin.site.urls),
    path("oidc/", include("oauth2_authcodeflow.urls")),
    path("forms/", include("form_manager.urls")),
    path("staff-prototype/", include("staff_prototype.urls")),
    path("staff/", include("staff_review.urls")),
    path("api/v1/", form_api.urls),
]

if apps.is_installed("pattern_library"):
    urlpatterns += [
        path("pattern-library/", include("pattern_library.urls")),
    ]
