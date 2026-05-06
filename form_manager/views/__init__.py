from form_manager.views.form_download import FormDownloadPDFView
from form_manager.views.form_edit import form_edit
from form_manager.views.form_finalize import form_finalize
from form_manager.views.form_review import form_review
from form_manager.views.form_views import *

__ALL__ = [
    "form_list",
    "form_start",
    form_edit.__name__,
    form_finalize.__name__,
    form_review.__name__,
    "FormPreviewView",
    "form_history",
    "FormSnapshotView",
    "form_lock",
    "form_unlock",
    "form_archive",
    "editing_lock_heartbeat",
    "editing_lock_release",
    FormDownloadPDFView.__name__,
]
