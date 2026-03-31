#!/bin/sh
# Creates S3 buckets in rustfs using AWS Signature V4 HMAC authentication.
# Requires: curl, openssl (both available in alpine).
set -e

ACCESS_KEY="${RUSTFS_ACCESS_KEY}"
SECRET_KEY="${RUSTFS_SECRET_KEY}"
HOST="${RUSTFS_HOST:-storage.csfeer:9000}"
REGION="${RUSTFS_REGION:-us-east-1}"
ENDPOINT="http://${HOST}"
BUCKET_TO_CREATE="${BUCKET_TO_CREATE}"

create_bucket() {
    BUCKET="$1"
    METHOD="PUT"
    URI="/${BUCKET}"
    DATE=$(date -u +%Y%m%d)
    DATETIME=$(date -u +%Y%m%dT%H%M%SZ)
    PAYLOAD_HASH=$(printf "" | openssl dgst -sha256 | awk '{print $2}')

    CANONICAL_HEADERS="host:${HOST}\nx-amz-content-sha256:${PAYLOAD_HASH}\nx-amz-date:${DATETIME}"
    SIGNED_HEADERS="host;x-amz-content-sha256;x-amz-date"

    CANONICAL_REQUEST="${METHOD}\n${URI}\n\n${CANONICAL_HEADERS}\n\n${SIGNED_HEADERS}\n${PAYLOAD_HASH}"
    CANONICAL_REQUEST_HASH=$(printf "${CANONICAL_REQUEST}" | openssl dgst -sha256 | awk '{print $2}')

    CREDENTIAL_SCOPE="${DATE}/${REGION}/s3/aws4_request"
    STRING_TO_SIGN="AWS4-HMAC-SHA256\n${DATETIME}\n${CREDENTIAL_SCOPE}\n${CANONICAL_REQUEST_HASH}"

    # Derive signing key via chained HMAC-SHA256
    DATE_KEY=$(printf "%s" "${DATE}" | openssl dgst -sha256 -mac HMAC -macopt "key:AWS4${SECRET_KEY}" | awk '{print $2}')
    DATE_REGION_KEY=$(printf "%s" "${REGION}" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_KEY}" | awk '{print $2}')
    DATE_REGION_SERVICE_KEY=$(printf "%s" "s3" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_REGION_KEY}" | awk '{print $2}')
    SIGNING_KEY=$(printf "%s" "aws4_request" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_REGION_SERVICE_KEY}" | awk '{print $2}')

    SIGNATURE=$(printf "${STRING_TO_SIGN}" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${SIGNING_KEY}" | awk '{print $2}')

    AUTHORIZATION="AWS4-HMAC-SHA256 Credential=${ACCESS_KEY}/${CREDENTIAL_SCOPE}, SignedHeaders=${SIGNED_HEADERS}, Signature=${SIGNATURE}"

    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "${ENDPOINT}/${BUCKET}" \
        -H "Host: ${HOST}" \
        -H "x-amz-date: ${DATETIME}" \
        -H "x-amz-content-sha256: ${PAYLOAD_HASH}" \
        -H "Authorization: ${AUTHORIZATION}")

    if [ "${HTTP_STATUS}" = "200" ] || [ "${HTTP_STATUS}" = "409" ]; then
        echo "Bucket '${BUCKET}' ready (HTTP ${HTTP_STATUS})"
    else
        echo "Failed to create bucket '${BUCKET}' (HTTP ${HTTP_STATUS})" >&2
        exit 1
    fi
}

create_service_account() {
    ADMIN_HOST="127.0.0.1:9001"
    METHOD="PUT"
    URI="/rustfs/admin/v3/add-service-accounts"
    PAYLOAD="{\"accessKey\":\"$IAM_KEY_TO_CREATE\",\"secretKey\":\"$IAM_SECRET_TO_CREATE\",\"name\":\"key\",\"description\":\"\",\"policy\":null,\"expiration\":\"9999-01-01T00:00:00.000Z\"}"
    DATE=$(date -u +%Y%m%d)
    DATETIME=$(date -u +%Y%m%dT%H%M%SZ)
    PAYLOAD_HASH=$(printf "%s" "${PAYLOAD}" | openssl dgst -sha256 | awk '{print $2}')

    CANONICAL_HEADERS="host:${ADMIN_HOST}\nx-amz-content-sha256:${PAYLOAD_HASH}\nx-amz-date:${DATETIME}"
    SIGNED_HEADERS="host;x-amz-content-sha256;x-amz-date"

    CANONICAL_REQUEST="${METHOD}\n${URI}\n\n${CANONICAL_HEADERS}\n\n${SIGNED_HEADERS}\n${PAYLOAD_HASH}"
    CANONICAL_REQUEST_HASH=$(printf "${CANONICAL_REQUEST}" | openssl dgst -sha256 | awk '{print $2}')

    CREDENTIAL_SCOPE="${DATE}/${REGION}/s3/aws4_request"
    STRING_TO_SIGN="AWS4-HMAC-SHA256\n${DATETIME}\n${CREDENTIAL_SCOPE}\n${CANONICAL_REQUEST_HASH}"

    DATE_KEY=$(printf "%s" "${DATE}" | openssl dgst -sha256 -mac HMAC -macopt "key:AWS4${SECRET_KEY}" | awk '{print $2}')
    DATE_REGION_KEY=$(printf "%s" "${REGION}" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_KEY}" | awk '{print $2}')
    DATE_REGION_SERVICE_KEY=$(printf "%s" "s3" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_REGION_KEY}" | awk '{print $2}')
    SIGNING_KEY=$(printf "%s" "aws4_request" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${DATE_REGION_SERVICE_KEY}" | awk '{print $2}')

    SIGNATURE=$(printf "${STRING_TO_SIGN}" | openssl dgst -sha256 -mac HMAC -macopt "hexkey:${SIGNING_KEY}" | awk '{print $2}')

    AUTHORIZATION="AWS4-HMAC-SHA256 Credential=${ACCESS_KEY}/${CREDENTIAL_SCOPE}, SignedHeaders=${SIGNED_HEADERS}, Signature=${SIGNATURE}"

    RESULT=$(curl -s -X PUT "http://${ADMIN_HOST}${URI}" \
        -H "Host: ${ADMIN_HOST}" \
        -H "x-amz-date: ${DATETIME}" \
        -H "x-amz-content-sha256: ${PAYLOAD_HASH}" \
        -H "Content-Type: application/json" \
        -H "Authorization: ${AUTHORIZATION}" \
        -d "${PAYLOAD}")
}

# Wait for rustfs to be ready
until sleep 2 && curl -sf "http://127.0.0.1:9001/health" > /dev/null 2>&1; do
    echo "Waiting for rustfs..."
    sleep 1
done

# Create buckets
create_bucket $BUCKET_TO_CREATE

# Create service account
create_service_account
