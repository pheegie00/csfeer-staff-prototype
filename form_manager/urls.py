from django.urls import path

from . import views

urlpatterns = [
    path("", views.form_list, name="form_list"),
    path("start/<str:form_id>/", views.form_start, name="form_start"),
    path("entry/<int:pk>/edit/", views.FormEditView.as_view(), name="form_edit"),
    path("entry/<int:pk>/preview/", views.FormPreviewView.as_view(), name="form_preview"),
    path("entry/<int:pk>/history/", views.form_history, name="form_history"),
    path(
        "entry/<int:pk>/snapshot/<int:audit_id>/",
        views.FormSnapshotView.as_view(),
        name="form_snapshot",
    ),
    path("entry/<int:pk>/lock/", views.form_lock, name="form_lock"),
    path("entry/<int:pk>/unlock/", views.form_unlock, name="form_unlock"),
    path("entry/<int:pk>/archive/", views.form_archive, name="form_archive"),
]
