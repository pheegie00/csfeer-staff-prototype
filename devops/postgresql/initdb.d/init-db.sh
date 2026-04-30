#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "csfeer_e2e_test";
    GRANT ALL PRIVILEGES ON DATABASE "csfeer_e2e_test" TO "$POSTGRES_USER";
EOSQL