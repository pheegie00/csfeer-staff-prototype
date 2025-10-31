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

# Test users (from devops/mocks/keycloak/users.csv)
TEST_USERS = {
    "admin": {
        "username": "admin",
        "password": "admin",  # Default password from Keycloak setup
        "roles": ["csfeer_admin", "csfeer_user"],
    },
    "demo": {
        "username": "demo",
        "password": "demo",
        "roles": ["csfeer_user"],
    },
    "demo-1": {
        "username": "demo-1",
        "password": "demo-1",
        "roles": ["csfeer_user"],
    },
    "demo-2": {
        "username": "demo-2",
        "password": "demo-2",
        "roles": ["csfeer_user"],
    },
}
