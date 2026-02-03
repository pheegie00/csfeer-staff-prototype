"""
AWS Secrets Manager integration for CSFeer.

This module provides utilities to fetch secrets from AWS Secrets Manager
when running in AWS environments (dev, staging, prod), and falls back to
environment variables/local .env files for local development.
"""

import json
import logging
import os
from functools import lru_cache
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)


class SecretsManagerError(Exception):
    """Raised when there's an error fetching secrets from AWS Secrets Manager."""

    pass


class SecretsManager:
    """
    Manages secret retrieval from AWS Secrets Manager.

    Provides caching and error handling for secret retrieval operations.
    """

    def __init__(self, region_name: str | None = None):
        """
        Initialize the SecretsManager.

        Args:
            region_name: AWS region name. If not provided, uses AWS_DEFAULT_REGION
                        or AWS_REGION environment variables.
        """
        self.region_name = (
            region_name or os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION", "us-east-1")
        )
        self._client = None

    @property
    def client(self):
        """Lazy-load the boto3 Secrets Manager client."""
        if self._client is None:
            try:
                self._client = boto3.client("secretsmanager", region_name=self.region_name)
            except Exception as e:
                logger.error(f"Failed to create Secrets Manager client: {e}")
                raise SecretsManagerError(
                    f"Failed to initialize AWS Secrets Manager client: {e}"
                ) from e
        return self._client

    def get_secret(self, secret_name: str, parse_json: bool = True) -> dict[str, Any] | str:
        """
        Retrieve a secret from AWS Secrets Manager.

        Args:
            secret_name: The name or ARN of the secret to retrieve
            parse_json: If True, parse the secret value as JSON (default: True)

        Returns:
            Parsed JSON dict if parse_json=True, otherwise raw string value

        Raises:
            SecretsManagerError: If the secret cannot be retrieved
        """
        try:
            logger.info(f"Fetching secret: {secret_name}")
            response = self.client.get_secret_value(SecretId=secret_name)

            # Secrets can be stored as SecretString or SecretBinary
            if "SecretString" in response:
                secret_value = response["SecretString"]
            else:
                secret_value = response["SecretBinary"].decode("utf-8")

            if parse_json:
                try:
                    return json.loads(secret_value)
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse secret as JSON: {secret_name}. Returning raw string."
                    )
                    return secret_value

            return secret_value

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise SecretsManagerError(f"Secret not found: {secret_name}") from e
            elif error_code == "InvalidRequestException":
                raise SecretsManagerError(f"Invalid request for secret: {secret_name}") from e
            elif error_code == "InvalidParameterException":
                raise SecretsManagerError(f"Invalid parameter for secret: {secret_name}") from e
            elif error_code == "DecryptionFailure":
                raise SecretsManagerError(f"Failed to decrypt secret: {secret_name}") from e
            elif error_code == "InternalServiceError":
                raise SecretsManagerError(
                    f"AWS internal service error for secret: {secret_name}"
                ) from e
            else:
                raise SecretsManagerError(f"Error retrieving secret {secret_name}: {e}") from e
        except (BotoCoreError, Exception) as e:
            raise SecretsManagerError(
                f"Unexpected error retrieving secret {secret_name}: {e}"
            ) from e

    def get_secret_value(self, secret_name: str, key: str, default: Any = None) -> Any:
        """
        Retrieve a specific key from a JSON secret.

        Args:
            secret_name: The name or ARN of the secret
            key: The key to extract from the JSON secret
            default: Default value if key is not found

        Returns:
            The value of the specified key, or default if not found

        Raises:
            SecretsManagerError: If the secret cannot be retrieved
        """
        secret_dict = self.get_secret(secret_name, parse_json=True)
        if not isinstance(secret_dict, dict):
            logger.warning(f"Secret {secret_name} is not a JSON object")
            return default
        return secret_dict.get(key, default)


@lru_cache(maxsize=32)
def get_cached_secret(secret_name: str, region_name: str | None = None) -> dict[str, Any] | str:
    """
    Retrieve and cache a secret from AWS Secrets Manager.

    This function uses LRU caching to avoid repeated API calls for the same secret
    within the application lifecycle.

    Args:
        secret_name: The name or ARN of the secret to retrieve
        region_name: AWS region name (optional)

    Returns:
        The secret value (dict if JSON, str otherwise)

    Raises:
        SecretsManagerError: If the secret cannot be retrieved
    """
    manager = SecretsManager(region_name=region_name)
    return manager.get_secret(secret_name)


def get_secret_or_env(
    secret_name: str | None,
    env_var: str,
    key: str | None = None,
    default: Any = None,
    use_secrets_manager: bool = True,
) -> Any:
    """
    Try to fetch from AWS Secrets Manager, fall back to environment variable.

    This is the primary function to use for retrieving configuration values that
    should come from Secrets Manager in production but environment variables locally.

    Args:
        secret_name: The name of the secret in AWS Secrets Manager (None to skip)
        env_var: The environment variable name to use as fallback
        key: Optional key to extract from JSON secret
        default: Default value if neither source provides a value
        use_secrets_manager: Whether to attempt Secrets Manager fetch (default: True)

    Returns:
        The configuration value from the first available source:
        1. AWS Secrets Manager (if enabled and secret_name provided)
        2. Environment variable
        3. Default value

    Example:
        >>> db_password = get_secret_or_env(
        ...     secret_name="csfeer-dev-db",
        ...     env_var="PGPASSWORD",
        ...     key="password",
        ...     default="local_password"
        ... )
    """
    # Try AWS Secrets Manager first if enabled and secret name provided
    if use_secrets_manager and secret_name:
        try:
            manager = SecretsManager()
            if key:
                return manager.get_secret_value(secret_name, key, default=None)
            else:
                return manager.get_secret(secret_name, parse_json=False)
        except SecretsManagerError as e:
            logger.warning(f"Failed to fetch from Secrets Manager: {e}. Falling back to env var.")

    # Fall back to environment variable
    env_value = os.getenv(env_var)
    if env_value is not None:
        return env_value

    # Return default if provided
    return default
