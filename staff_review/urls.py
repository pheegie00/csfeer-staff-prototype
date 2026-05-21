from django.urls import path

from staff_review.views import (
    DeterminationRecordView,
    DeterminationView,
    InboxView,
    RationaleView,
    ReturnBuilderView,
    ReturnSendView,
    SubmissionDetailView,
    SubmissionEditView,
    SubmissionSaveEditView,
)

app_name = "staff_review"

urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),

    # Submission detail (review + edit-on-behalf)
    path("sub/<str:sub_id>/", SubmissionDetailView.as_view(), name="submission_detail"),
    path("sub/<str:sub_id>/edit/", SubmissionEditView.as_view(), name="submission_edit"),
    path("sub/<str:sub_id>/save-edit/", SubmissionSaveEditView.as_view(), name="submission_save_edit"),
    path("sub/<str:sub_id>/rationale/", RationaleView.as_view(), name="rationale"),

    # Return for revision
    path("sub/<str:sub_id>/return/", ReturnBuilderView.as_view(), name="return_builder"),
    path("sub/<str:sub_id>/return/send/", ReturnSendView.as_view(), name="return_send"),

    # Determination
    path("sub/<str:sub_id>/determination/", DeterminationView.as_view(), name="determination"),
    path("sub/<str:sub_id>/determination/record/", DeterminationRecordView.as_view(), name="determination_record"),
]
