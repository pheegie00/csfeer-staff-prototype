from django.urls import path

from staff_review.views import InboxView

app_name = "staff_review"

urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
]
