from django.urls import path

from . import views

urlpatterns = [
    path("", views.form_list, name="form_list"),
    path("start/<uuid:form_id>/", views.form_start, name="form_start"),
    path(
        "entry/<uuid:pk>/edit-legacy/", views.FormEditLegacyView.as_view(), name="form_edit_legacy"
    ),
    path("entry/<uuid:pk>/edit/", views.form_edit, name="form_edit"),
    path("entry/<uuid:pk>/preview/", views.FormPreviewView.as_view(), name="form_preview"),
    path("entry/<uuid:pk>/history/", views.form_history, name="form_history"),
    path(
        "entry/<uuid:pk>/snapshot/<uuid:audit_id>/",
        views.FormSnapshotView.as_view(),
        name="form_snapshot",
    ),
    path("entry/<uuid:pk>/lock/", views.form_lock, name="form_lock"),
    path("entry/<uuid:pk>/unlock/", views.form_unlock, name="form_unlock"),
    path("entry/<uuid:pk>/archive/", views.form_archive, name="form_archive"),
    path(
        "entry/<uuid:pk>/download/", views.FormDownloadPDFView.as_view(), name="form_download_pdf"
    ),
]
