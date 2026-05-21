from django.urls import path

from staff_review.demo_views import DemoUsersIndexView, ViewAsUserView
from staff_review.form_builder_views import (
    FormBuilderDetailView,
    FormBuilderListView,
    FormScopingEditView,
    PublishNewVersionView,
    SubmissionWindowEditView,
)
from staff_review.views import (
    AuditLogView,
    CSVExportView,
    DeterminationRecordView,
    DeterminationView,
    ExportsIndexView,
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

    # Exports (CORE-46) -- CSV export of resolved submissions
    path("exports/", ExportsIndexView.as_view(), name="exports"),
    path("exports/csv/", CSVExportView.as_view(), name="export_csv"),

    # System audit log (CORE-47) -- FISMA / NIST 800-53 compliance viewer
    path("audit-log/", AuditLogView.as_view(), name="audit_log"),

    # Form Builder (Batch E.2) -- program-scoped form template management
    path("form-builder/", FormBuilderListView.as_view(), name="form_builder_list"),
    path("form-builder/<uuid:form_def_id>/", FormBuilderDetailView.as_view(), name="form_builder_detail"),
    # Batch F -- CORE-25 (submission windows) + CORE-22 (org scoping)
    path("form-builder/<uuid:form_def_id>/window/", SubmissionWindowEditView.as_view(), name="form_builder_window_edit"),
    path("form-builder/<uuid:form_def_id>/scope/", FormScopingEditView.as_view(), name="form_builder_scope_edit"),
    # Batch G -- CORE-23/24 (publish new version + auto-close deprecated)
    path("form-builder/<uuid:form_def_id>/publish/", PublishNewVersionView.as_view(), name="form_builder_publish"),

    # Phase 4 Step 7 -- View-as impersonation for demo / testing (superuser-only)
    path("demo-users/", DemoUsersIndexView.as_view(), name="demo_users_index"),
    path("demo-users/view-as/", ViewAsUserView.as_view(), name="view_as_user"),
]
