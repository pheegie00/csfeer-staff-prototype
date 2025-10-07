from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class OIDCConfig(BaseModel):
    client_id: str = "csfeer-auth"
    client_secret: str = ""
    force_secret_with_pkce: bool = True
    document_url: str = "http://oauth.csfeer:8081/realms/csfeer/.well-known/openid-configuration"
    scopes: list[str] = ["openid", "email", "profile", "roles", "offline_access"]
    no_auth_urls: list[str] = ["api/", "logged-out"]


class DBConfig(BaseModel):
    use_iam_auth: bool = False
    pgdatabase: str = "csfeer"
    pguser: str = "csfeer"
    pgpassword: str = "secret123"
    pgport: str = "5432"
    pghost: str = "localhost"
    statement_timeout: int = 3600000
    ssl_mode: str = "require"


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore", env_nested_delimiter="__"
    )
    secret_key: str = "REPLACE ME"
    debug: bool = True
    allowed_hosts: list[str] = ["localhost", "0.0.0.0", "ui.csfeer", "127.0.0.1"]
    time_zone: str = "EST"
    language_code: str = "en-us"
    use_i18n: bool = True
    use_tz: bool = True
    oidc_config: OIDCConfig = OIDCConfig()
    db_config: DBConfig = DBConfig()
    environment: str = "local"
    api_key: str = "SECRET123"

    @property
    def is_local(self) -> bool:
        return self.environment == "local"


def get_app_config() -> AppConfig:
    return AppConfig()
