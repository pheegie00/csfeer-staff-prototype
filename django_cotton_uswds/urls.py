from django.urls import path

from . import views

app_name = "django_cotton_uswds"

urlpatterns = [
    # Dev-only component gallery
    path("dev/components/", views.component_gallery, name="component_gallery"),
]
