import uuid

from django.contrib.auth import get_user_model
from django.db import models

from organizations.models import BaseModel

User = get_user_model()


class FormEditingLock(BaseModel):
    form_entry = models.OneToOneField(
        "form_manager.FormEntry", on_delete=models.CASCADE, related_name="editing_lock"
    )
    locked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    lock_token = models.UUIDField(default=uuid.uuid4)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_entry} locked by {self.locked_by}"
