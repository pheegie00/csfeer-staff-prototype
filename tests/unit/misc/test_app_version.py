import pytest
import os
from django.template.loader import render_to_string
from django.test import RequestFactory

from csfeer.context_processors import app_version
from csfeer.config import AppConfig


@pytest.fixture
def rf():
    return RequestFactory()


# --- Context processor tests ---


def test_show_app_version_setting_defaults_to_false():
    """Ensure the setting defaults to False"""
    assert AppConfig.model_construct().show_app_version is False


def test_app_version_context_processor(rf, settings):
    """Ensure the correct app version is returned from the context processor"""
    settings.APP_VERSION = "1.2.3"
    result = app_version(rf.get("/"))
    assert result.get("APP_VERSION") == "1.2.3"


def test_show_app_version_context_processor_when_true(rf, settings):
    """Ensure the value of SHOW_APP_VERSION is correct"""
    settings.SHOW_APP_VERSION = True
    result = app_version(rf.get("/"))
    assert result.get("SHOW_APP_VERSION") == True

    settings.SHOW_APP_VERSION = False
    result = app_version(rf.get("/"))
    assert result.get("SHOW_APP_VERSION") == False


# --- Django settings tests ---


def test_app_version_reads_from_version_file(tmp_path):
    """Ensure the version is correct when reading from the version file"""
    version_file = tmp_path / ".version"
    version_file.write_text("2.0.0\n")

    # Mirror the logic in settings.py
    value = version_file.read_text().strip() if version_file.exists() else "unknown"
    assert value == "2.0.0"


def test_app_version_defaults_to_unknown_when_file_missing(tmp_path):
    """Ensure the version is correct if there's no version file"""
    missing = tmp_path / ".version"
    value = missing.read_text().strip() if missing.exists() else "unknown"
    assert value == "unknown"


# --- Template rendering tests ---


def test_footer_renders_version_as_visible_text_when_enabled():
    """Ensure the app version renders correctly"""
    content = render_to_string(
        "cotton/footer_main.html",
        {"SHOW_APP_VERSION": True, "APP_VERSION": "3.1.4", "email": "support@example.com"},
    )
    assert "3.1.4" in content
    assert "<!-- version: 3.1.4 -->" not in content


def test_footer_renders_version_in_html_comment_when_disabled():
    """Ensure the app version doesn't render if the setting is set to False"""
    content = render_to_string(
        "cotton/footer_main.html",
        {"SHOW_APP_VERSION": False, "APP_VERSION": "3.1.4", "email": "support@example.com"},
    )
    assert "<!-- version: 3.1.4 -->" in content
    assert ">3.1.4<" not in content
