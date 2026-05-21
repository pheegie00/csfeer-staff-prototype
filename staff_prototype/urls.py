from django.urls import path

from staff_prototype.views import PrototypeIndex

app_name = "staff_prototype"

urlpatterns = [
    path("", PrototypeIndex.as_view(), name="index"),
]
