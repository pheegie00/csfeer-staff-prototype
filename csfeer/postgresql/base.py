from typing import Any

import boto3  # type: ignore
from django.db.backends.postgresql import base

from csfeer.config import get_app_config


class DatabaseWrapper(base.DatabaseWrapper):

    def get_connection_params(self) -> dict[str, Any]:  # type: ignore
        config = get_app_config()
        params = super().get_connection_params() or {}
        params.update(
            {
                "dbname": config.db_config.pgdatabase,
                "user": config.db_config.pguser,
                "port": config.db_config.pgport,
                "host": config.db_config.pghost,
            }
        )
        if config.db_config.use_iam_auth:
            rds_client = boto3.client("rds")
            params["password"] = rds_client.generate_db_auth_token(
                DBHostname=config.db_config.pghost,
                Port=config.db_config.pgport,
                DBUsername=config.db_config.pguser,
            )
            params["connect_timeout"] = str(60 * 14)
        else:
            params["password"] = config.db_config.pgpassword

        return params
        return params
