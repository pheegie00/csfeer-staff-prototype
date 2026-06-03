from django.urls import path
from django.views.generic import RedirectView

from form_manager import views
from form_manager.views.formspec_preview import formspec_preview

urlpatterns = [
    path("", views.form_list, name="form_list"),
    path("start/<uuid:form_id>/", views.form_start, name="form_start"),
    path("entry/<uuid:pk>/edit/", views.form_edit, name="form_edit"),
    # STAFF-MP-13: schema-driven parallel render route (gated by form_runtime flag).
    path("entry/<uuid:pk>/render/", formspec_preview, name="form_render"),
    # Back-compat: the route used to be /formspec-preview/; redirect to /render/.
    path(
        "entry/<uuid:pk>/formspec-preview/",
        RedirectView.as_view(url="/forms/entry/%(pk)s/render/", permanent=False),
    ),
    path("entry/<uuid:pk>/review/", views.form_review, name="form_review"),
    path("entry/<uuid:pk>/finalize/", views.form_finalize, name="form_finalize"),
    path("entry/<uuid:pk>/preview/", views.FormPreviewView.as_view(), name="form_preview"),
    path("entry/<uuid:pk>/history/", views.form_history, name="form_history"),
    path(
        "entry/<uuid:pk>/snapshot/<uuid:audit_id>/",
        views.FormSnapshotView.as_view(),
        name="form_snapshot",
    ),
    path("entry/<uuid:pk>/lock/", views.form_lock, name="form_lock"),
    path("entry/<uuid:pk>/unlock/", views.form_unlock, name="form_unlock"),
    path(
        "entry/<uuid:pk>/editing-lock/heartbeat/",
        views.editing_lock_heartbeat,
        name="editing_lock_heartbeat",
    ),
    path(
        "entry/<uuid:pk>/editing-lock/release/",
        views.editing_lock_release,
        name="editing_lock_release",
    ),
    path("entry/<uuid:pk>/archive/", views.form_archive, name="form_archive"),
    path(
        "entry/<uuid:pk>/download/", views.FormDownloadPDFView.as_view(), name="form_download_pdf"
    ),
]
