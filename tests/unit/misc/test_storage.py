import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from csfeer.config import AppConfig

config = AppConfig()


@pytest.mark.integration
def test_default_storage_upload_and_exists(settings):
    """Ensure the default storage backend can save a file and report it as existing."""

    file_name = "test-uploads/test_storage_check.txt"
    file_content = ContentFile(b"hello storage")

    saved_name = default_storage.save(file_name, file_content)

    try:
        assert default_storage.exists(saved_name)
    finally:
        default_storage.delete(saved_name)
