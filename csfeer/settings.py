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
    "django_extensions",
    # Local
    "core",
    "users",
    "form_manager",
    "organizations",
    "programs",
    "staff_prototype",
    "staff_review",
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

AUTHENTICATION_BACKENDS = [
    "csfeer.auth_backends.EmailOIDCAuthenticationBackend",
    "csfeer.auth_backends.FormPermissionBackend",
]

# Deployment fallback: when no Keycloak is reachable (the OIDC discovery
# URL is empty OR points at the local-only hostnames), strip the OIDC
# middleware and add Django's ModelBackend so password login works. Used
# for the Fly.io demo deploy until we get Keycloak up in front of it.
_oidc_url = (settings.oidc_config.document_url or "").lower()
_oidc_is_local_only = (
    not _oidc_url
    or "oauth.csfeer" in _oidc_url
    or "localhost" in _oidc_url
    or "127.0.0.1" in _oidc_url
)
if _oidc_is_local_only and settings.is_production:
    MIDDLEWARE = [m for m in MIDDLEWARE if "oauth2_authcodeflow" not in m]
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "csfeer.auth_backends.FormPermissionBackend",
    ]
    LOGIN_URL = "/admin/login/"
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
                "csfeer.context_processors.app_version",
                "staff_review.context_processors.staff_persona",
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


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_STORAGE_BUCKET_NAME = settings.aws_storage_bucket_name
AWS_S3_ENDPOINT_URL = settings.aws_s3_endpoint_url


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
        "TEST": {"NAME": settings.db_config.test_pgdatabase},
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
OIDC_RP_USE_PKCE = settings.oidc_config.use_pkce
OIDC_MIDDLEWARE_NO_AUTH_URL_PATTERNS = settings.oidc_config.no_auth_urls
OIDC_OP_EXPECTED_EMAIL_CLAIM = "email"

OIDC_EXTEND_USER = (
    "csfeer.auth_backends.extend_user_with_roles"  # Custom function to extend user with roles
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
        "django.security.DisallowedHost": {
            "handlers": ["file"],
            "propagate": False,
        },
    },
}

USE_THOUSAND_SEPARATOR = True

_version_file = BASE_DIR / ".version"
APP_VERSION = _version_file.read_text().strip() if _version_file.exists() else "unknown"

CSRF_TRUSTED_ORIGINS = settings.csrf_trusted_origins

# Production safety. Fly terminates TLS at the edge and forwards HTTP
# internally with `X-Forwarded-Proto: https`, so we have to tell Django
# to trust that header for is_secure() to return True. Also enforce
# secure cookies + HSTS in production.
if settings.is_production:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7  # 1 week, easy to roll back
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    # Conservative whitelist: allow any *.fly.dev origin so we don't have to
    # re-deploy when the app gets renamed. Plus whatever the user configures.
    CSRF_TRUSTED_ORIGINS = list(settings.csrf_trusted_origins) + [
        "https://*.fly.dev",
    ]

AWS_S3_SIGNATURE_VERSION = "s3v4"

SHOW_APP_VERSION = settings.show_app_version

LOCK_DURATION_MINUTES = settings.lock_duration_minutes
