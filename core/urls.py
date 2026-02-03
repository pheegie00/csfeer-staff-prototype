"""URL configuration for core app."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("health/", views.health_check, name="health"),
    path("ready/", views.readiness_check, name="ready"),
]
