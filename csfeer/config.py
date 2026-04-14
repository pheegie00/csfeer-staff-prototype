from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class OIDCConfig(BaseModel):
    client_id: str = "csfeer-auth"
    client_secret: str = ""
    force_secret_with_pkce: bool = True
    document_url: str = "http://oauth.csfeer:8081/realms/csfeer/.well-known/openid-configuration"
    scopes: list[str] = ["openid", "email", "profile", "phone", "roles", "offline_access"]
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
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore", env_nested_delimiter="__"
    )
    secret_key: str = "REPLACE ME"
    debug: bool = True
    allowed_hosts: list[str] = ["localhost", "0.0.0.0", "ui.csfeer", "127.0.0.1"]
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

    @property
    def is_local(self) -> bool:
        return self.environment == "local"

    @property
    def is_production(self) -> bool:
        return self.environment in ["production", "prod"]


def get_app_config() -> AppConfig:
    return AppConfig()
