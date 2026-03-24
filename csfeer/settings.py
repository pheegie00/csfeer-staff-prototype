"""
Django settings for the Community Outcomes Reporting Engine (CORE) project.
"""

import os
from pathlib import Path

from csfeer.config import AppConfig

settings = AppConfig()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.debug

ALLOWED_HOSTS = settings.allowed_hosts


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "oauth2_authcodeflow",
    "pattern_library",
    "crispy_forms",
    "django_cotton",
    "django_cotton_uswds",
    "django_json_widget",
    # Local
    "core",
    "users",
    "form_manager",
    "django.forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "oauth2_authcodeflow.middleware.LoginRequiredMiddleware",
    "oauth2_authcodeflow.middleware.RefreshAccessTokenMiddleware",
    "oauth2_authcodeflow.middleware.RefreshSessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = ["csfeer.backends.EmailOIDCAuthenticationBackend"]
ROOT_URLCONF = "csfeer.urls"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "csfeer", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "pattern_library.loader_tags",
                "django_cotton_uswds.templatetags.cotton_aliases",
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = "uswds"
CRISPY_ALLOWED_TEMPLATE_PACKS = ("uni_form", "uswds")

STATIC_URL = "/static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [
    BASE_DIR / "csfeer" / "static",  # Where Django looks for static files
]
STATIC_ROOT = BASE_DIR / "staticfiles"
NPM_ROOT_PATH = str(BASE_DIR / "csfeer")  # Where your package.json is located
NPM_FILE_PATTERNS = {
    "@uswds/uswds": [
        "dist/css/*.css",
        "dist/js/*.js",
        "dist/js/*.map",
        "dist/fonts/**/*",
        "dist/img/**/*",
    ],
    "alpinejs": ["dist/*.js"],
    "htmx.org": ["dist/*.js"],
    "htmx-ext-sse": ["dist/*.js"],
}

WSGI_APPLICATION = "csfeer.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "csfeer.postgresql",
        "NAME": settings.db_config.pgdatabase,
        "CONN_MAX_AGE": 60 * 14,  # IAM password tokens only last 15 minutes
        "CONN_HEALTH_CHECKS": True,
        "POOL": True,
        "OPTIONS": {
            "sslmode": settings.db_config.ssl_mode,
            "options": f"-c statement_timeout={settings.db_config.statement_timeout}",
        },
        "USER": settings.db_config.pguser,
        "PASSWORD": settings.db_config.pgpassword,
        "HOST": settings.db_config.pghost,
        "PORT": settings.db_config.pgport,
    }
}

# Django App Configuration
SECRET_KEY = settings.secret_key
LANGUAGE_CODE = settings.language_code
TIME_ZONE = settings.time_zone
USE_I18N = settings.use_i18n
USE_TZ = settings.use_tz

# OIDC Configuration
OIDC_OP_DISCOVERY_DOCUMENT_URL = settings.oidc_config.document_url
OIDC_RP_CLIENT_ID = settings.oidc_config.client_id
OIDC_RP_CLIENT_SECRET = settings.oidc_config.client_secret
OIDC_RP_FORCE_SECRET_WITH_PKCE = settings.oidc_config.force_secret_with_pkce
OIDC_RP_SCOPES = settings.oidc_config.scopes
OIDC_MIDDLEWARE_NO_AUTH_URL_PATTERNS = settings.oidc_config.no_auth_urls
OIDC_EXTEND_USER = (
    "csfeer.backends.extend_user_with_roles"  # Custom function to extend user with roles
)

PATTERN_LIBRARY = {
    "SECTIONS": (
        ("Components", ["patterns/components"]),
        ("Pages", ["patterns/pages"]),
    ),
    "TEMPLATE_SUFFIX": ".html",
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
}

if DEBUG:
    X_FRAME_OPTIONS = "SAMEORIGIN"


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CoreUser"

# Logging Configuration
# https://docs.djangoproject.com/en/5.2/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "WARNING" if settings.is_production else ("DEBUG" if DEBUG else "INFO"),
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "maxBytes": settings.logging_config.file_max_bytes,
            "backupCount": settings.logging_config.file_backup_count,
            "formatter": "verbose",
            "level": "DEBUG",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django_errors.log",
            "maxBytes": settings.logging_config.file_max_bytes,
            "backupCount": settings.logging_config.file_backup_count,
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": settings.logging_config.level,
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": settings.logging_config.level,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file", "error_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "DEBUG" if DEBUG and settings.is_local else "INFO",
            "propagate": False,
        },
    },
}

USE_THOUSAND_SEPARATOR = True
