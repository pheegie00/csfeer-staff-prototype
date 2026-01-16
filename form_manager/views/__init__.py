from form_manager.views.form_download import FormDownloadPDFView
from form_manager.views.form_edit import form_edit
from form_manager.views.form_finalize import form_finalize
from form_manager.views.form_review import form_review
from form_manager.views.form_views import *

__ALL__ = [
    "form_list",
    "form_start",
    "form_edit",
    "form_finalize",
    "form_review",
    "FormPreviewView",
    "form_history",
    "FormSnapshotView",
    "form_lock",
    "form_unlock",
    "form_archive",
    "FormDownloadPDFView",
]
