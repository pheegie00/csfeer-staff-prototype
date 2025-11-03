"""
Playwright configuration for e2e tests.
This file provides additional configuration beyond pytest settings.
"""

import os

# Base URL for the application
BASE_URL = os.environ.get("BASE_URL", "http://ui.csfeer:8000")

# Browser configuration
BROWSER_CONFIG = {
    "headless": True,
    "viewport": {"width": 1920, "height": 1080},
    "locale": "en-US",
    "timezone_id": "America/New_York",
    "ignore_https_errors": True,
}

# Test configuration
TEST_CONFIG = {
    "timeout": 30000,  # 30 seconds
    "navigation_timeout": 30000,
    "expect_timeout": 5000,
}

# Video recording
VIDEO_CONFIG = {
    "record_video_dir": "tests/videos/",
    "record_video_size": {"width": 1920, "height": 1080},
}

# Trace recording
TRACE_CONFIG = {
    "screenshots": True,
    "snapshots": True,
    "sources": True,
}

# Test users (imported from tests/fixtures/users.py)
