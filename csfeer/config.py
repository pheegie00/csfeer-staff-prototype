import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OIDCConfig(BaseModel):
    client_id: str = "csfeer-auth"
    client_secret: str = ""
    force_secret_with_pkce: bool = True
    document_url: str = "http://oauth.csfeer:8081/realms/csfeer/.well-known/openid-configuration"
    scopes: list[str] = [
        "openid",
        "email",
        "profile",
        "phone",
        "offline_access",
    ]
    no_auth_urls: list[str] = ["api/", "logged-out", "login-error", "^/$"]
    use_pkce: bool = True


class DBConfig(BaseModel):
    use_iam_auth: bool = False
    pgdatabase: str = "csfeer"
    test_pgdatabase: str = "test_csfeer"
    pguser: str = "csfeer"
    pgpassword: str = "secret123"
    pgport: str = "5432"
    pghost: str = "localhost"
    statement_timeout: int = 3600000
    ssl_mode: str = "require"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file_max_bytes: int = 10485760  # 10 MB
    file_backup_count: int = 5


class AppConfig(BaseSettings):
    # Resolve .env path relative to THIS file (csfeer/config.py) so it works
    # regardless of where Python is launched from -- previously "../.env" was
    # interpreted relative to the CWD and silently broke when running manage.py
    # commands from the repo root.
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
    secret_key: str = "REPLACE ME"
    debug: bool = True
    allowed_hosts: list[str] = ["localhost", "0.0.0.0", "ui.csfeer", "ui.core", "127.0.0.1"]
    time_zone: str = "America/New_York"
    language_code: str = "en-us"
    use_i18n: bool = True
    use_tz: bool = True
    oidc_config: OIDCConfig = OIDCConfig()
    db_config: DBConfig = DBConfig()
    logging_config: LoggingConfig = LoggingConfig()
    environment: str = "local"
    api_key: str = "SECRET123"
    aws_storage_bucket_name: str = "core-local"
    aws_s3_endpoint_url: str | None = None
    csrf_trusted_origins: list[str] = ["https://*.acf.gov"]
    show_app_version: bool = Field(
        default=False, description="Whether to display the app version in the footer or not."
    )
    lock_duration_minutes: int = 15

    @property
    def is_local(self) -> bool:
        return self.environment == "local"

    @property
    def is_production(self) -> bool:
        return self.environment in ["production", "prod"]

    # Fly Postgres (and most PaaS Postgres providers) sets a single
    # DATABASE_URL env var like:
    #   postgres://user:pass@host:5432/dbname
    # Translate that into the granular DBConfig fields so the rest of
    # settings.py doesn't have to change. Explicit DB_CONFIG__* env vars
    # always win over DATABASE_URL.
    @model_validator(mode="after")
    def _hydrate_db_config_from_database_url(self):
        database_url = os.environ.get("DATABASE_URL", "").strip()
        if not database_url:
            return self
        try:
            parsed = urlparse(database_url)
        except ValueError:
            return self
        if not parsed.hostname:
            return self
        # Only fill in fields the user hasn't already overridden via
        # DB_CONFIG__* env vars (pydantic-settings has already applied
        # those by the time the validator runs).
        if "DB_CONFIG__PGHOST" not in os.environ:
            self.db_config.pghost = parsed.hostname
        if "DB_CONFIG__PGPORT" not in os.environ and parsed.port:
            self.db_config.pgport = str(parsed.port)
        if "DB_CONFIG__PGUSER" not in os.environ and parsed.username:
            self.db_config.pguser = unquote(parsed.username)
        if "DB_CONFIG__PGPASSWORD" not in os.environ and parsed.password:
            self.db_config.pgpassword = unquote(parsed.password)
        if "DB_CONFIG__PGDATABASE" not in os.environ and parsed.path:
            self.db_config.pgdatabase = parsed.path.lstrip("/")
        return self


def get_app_config() -> AppConfig:
    return AppConfig()
