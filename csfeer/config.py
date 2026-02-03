from typing import Any

from pydantic import BaseModel, Field
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


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file_max_bytes: int = 10485760  # 10 MB
    file_backup_count: int = 5


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore", env_nested_delimiter="__"
    )

    # AWS Secrets Manager Configuration
    use_secrets_manager: bool = Field(
        default=False,
        description="Enable AWS Secrets Manager for production secrets",
    )
    aws_secret_name: str = Field(
        default="",
        description="Name of the secret in AWS Secrets Manager (e.g., 'csfeer-dev-secrets')",
    )
    aws_db_secret_name: str = Field(
        default="",
        description="Name of the database secret in AWS Secrets Manager",
    )
    aws_region: str = Field(
        default="us-east-1",
        description="AWS region for Secrets Manager",
    )

    # Application Configuration
    secret_key: str = "REPLACE ME"
    debug: bool = True
    allowed_hosts: list[str] = ["localhost", "0.0.0.0", "ui.csfeer", "127.0.0.1"]
    csrf_trusted_origins: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    time_zone: str = "EST"
    language_code: str = "en-us"
    use_i18n: bool = True
    use_tz: bool = True
    use_oidc: bool = True  # Set to False to use Django auth instead
    oidc_config: OIDCConfig = OIDCConfig()
    db_config: DBConfig = DBConfig()
    logging_config: LoggingConfig = LoggingConfig()
    environment: str = "local"
    api_key: str = "SECRET123"

    def __init__(self, **data: Any):
        """Initialize AppConfig and load secrets from AWS Secrets Manager if enabled."""
        super().__init__(**data)

        # Load secrets from AWS Secrets Manager if enabled
        if self.use_secrets_manager:
            self._load_secrets_from_aws()

    def _load_secrets_from_aws(self) -> None:
        """
        Load secrets from AWS Secrets Manager and update configuration.

        This method is called automatically when use_secrets_manager is True.
        It fetches secrets from AWS and overrides the configuration values.
        """
        try:
            from csfeer.secrets_manager import SecretsManager, SecretsManagerError

            manager = SecretsManager(region_name=self.aws_region)

            # Load main application secrets
            if self.aws_secret_name:
                try:
                    app_secrets = manager.get_secret(self.aws_secret_name, parse_json=True)
                    if isinstance(app_secrets, dict):
                        # Update Django secret key
                        if "SECRET_KEY" in app_secrets:
                            self.secret_key = app_secrets["SECRET_KEY"]

                        # Update OIDC client secret
                        if "OIDC_CLIENT_SECRET" in app_secrets:
                            self.oidc_config.client_secret = app_secrets["OIDC_CLIENT_SECRET"]

                        # Update API key
                        if "API_KEY" in app_secrets:
                            self.api_key = app_secrets["API_KEY"]

                        # Update any other application secrets
                        if "DEBUG" in app_secrets:
                            self.debug = str(app_secrets["DEBUG"]).lower() in ["true", "1", "yes"]

                        if "ALLOWED_HOSTS" in app_secrets:
                            hosts = app_secrets["ALLOWED_HOSTS"]
                            if isinstance(hosts, str):
                                self.allowed_hosts = [h.strip() for h in hosts.split(",")]
                            elif isinstance(hosts, list):
                                self.allowed_hosts = hosts

                        if "CSRF_TRUSTED_ORIGINS" in app_secrets:
                            origins = app_secrets["CSRF_TRUSTED_ORIGINS"]
                            if isinstance(origins, str):
                                self.csrf_trusted_origins = [o.strip() for o in origins.split(",")]
                            elif isinstance(origins, list):
                                self.csrf_trusted_origins = origins

                except SecretsManagerError as e:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to load application secrets from AWS: {e}")

            # Load database secrets
            if self.aws_db_secret_name:
                try:
                    db_secrets = manager.get_secret(self.aws_db_secret_name, parse_json=True)
                    if isinstance(db_secrets, dict):
                        # AWS RDS secrets typically use these keys
                        if "username" in db_secrets:
                            self.db_config.pguser = db_secrets["username"]
                        if "password" in db_secrets:
                            self.db_config.pgpassword = db_secrets["password"]
                        if "host" in db_secrets:
                            self.db_config.pghost = db_secrets["host"]
                        if "port" in db_secrets:
                            self.db_config.pgport = str(db_secrets["port"])
                        if "dbname" in db_secrets:
                            self.db_config.pgdatabase = db_secrets["dbname"]

                except SecretsManagerError as e:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to load database secrets from AWS: {e}")

        except ImportError:
            import logging

            logger = logging.getLogger(__name__)
            logger.error("Failed to import secrets_manager module. AWS Secrets Manager disabled.")

    @property
    def is_local(self) -> bool:
        return self.environment == "local"

    @property
    def is_production(self) -> bool:
        return self.environment in ["production", "prod"]

    @property
    def is_aws_environment(self) -> bool:
        """Check if running in an AWS environment (dev, staging, prod)."""
        return self.environment in ["dev", "development", "staging", "stage", "production", "prod"]


def get_app_config() -> AppConfig:
    return AppConfig()
