#!/usr/bin/env bash
set -euo pipefail

# Config (overridable via env)
KC_URL=${KC_URL:-http://oauth.csfeer:8081}
REALM=${REALM:-csfeer}
KC_BOOT_USER=${KEYCLOAK_ADMIN:-admin}
KC_BOOT_PASS=${KEYCLOAK_ADMIN_PASSWORD:-admin}
USERS_CSV=${USERS_CSV:-}

# CSV-only user seeding; no env-based fallback

# Client to update with secret
OIDC_CLIENT_ID=${OIDC_CLIENT_ID:-csfeer-auth}
OIDC_CLIENT_SECRET=${OIDC_CLIENT_SECRET:-shhhhhhhh}

SETUP_COMPLETE_FILE_PATH="/opt/keycloak/setup-complete"

echo "[keycloak-setup] Waiting for Keycloak at ${KC_URL}..."
sleep 10

if [ -f "$SETUP_COMPLETE_FILE_PATH" ]; then
    echo "Setup previously completed, so skipping..."
    exit 0
fi


echo "[keycloak-setup] Authenticating admin user..."
/opt/keycloak/bin/kcadm.sh config credentials \
  --server "${KC_URL}" \
  --realm master \
  --user "${KC_BOOT_USER}" \
  --password "${KC_BOOT_PASS}"

ensure_user() {
  local USERNAME="$1" PASSWORD="$2" EMAIL="$3" FIRST="$4" LAST="$5"
  echo "[keycloak-setup] Ensuring user '${USERNAME}' exists in realm '${REALM}'..."
  if ! /opt/keycloak/bin/kcadm.sh get users -r "${REALM}" -q username="${USERNAME}" --fields username | grep -q "\"${USERNAME}\""; then
    /opt/keycloak/bin/kcadm.sh create users \
      -r "${REALM}" \
      -s username="${USERNAME}" \
      -s enabled=true \
      -s email="${EMAIL}" \
      -s emailVerified=true \
      -s firstName="${FIRST}" \
      -s lastName="${LAST}" \
      -o --fields id,username || true
  fi
  echo "[keycloak-setup] Setting password for '${USERNAME}'..."
  /opt/keycloak/bin/kcadm.sh set-password \
    -r "${REALM}" \
    --username "${USERNAME}" \
    --new-password "${PASSWORD}"
}

assign_roles() {
  local USERNAME="$1" ROLES_CSV="$2"
  IFS=',' read -r -a ROLES <<< "${ROLES_CSV}"
  local ARGS=( -r "${REALM}" --user "${USERNAME}" )
  for role in "${ROLES[@]}"; do
    # trim whitespace around role names
    local CLEAN_ROLE
    CLEAN_ROLE=$(echo "${role}" | sed 's/^ *//;s/ *$//')
    [[ -z "${CLEAN_ROLE}" ]] && continue
    ARGS+=( --rolename "${CLEAN_ROLE}" )
  done
  echo "[keycloak-setup] Assigning roles to '${USERNAME}': ${ROLES_CSV}"
  /opt/keycloak/bin/kcadm.sh add-roles "${ARGS[@]}" || true
}

# If a CSV is provided, seed users from it; otherwise fall back to env-based seeding
if [[ -n "${USERS_CSV}" ]] && [[ -f "${USERS_CSV}" ]]; then
  echo "[keycloak-setup] Seeding users from CSV: ${USERS_CSV}"
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Trim
    line=$(echo "$line" | sed 's/^\s*//;s/\s*$//')
    # Skip empty or commented lines
    [[ -z "$line" ]] && continue
    [[ "$line" =~ ^# ]] && continue
    # Allow header detection
    shopt -s nocasematch
    if [[ "$line" == user*name* || "$line" == username*roles* ]]; then
      continue
    fi
    shopt -u nocasematch
    # Split on first comma: username, roles
    USERNAME=${line%%,*}
    ROLES=${line#*,}
    USERNAME=$(echo "$USERNAME" | sed 's/^ *//;s/ *$//')
    ROLES=$(echo "$ROLES" | sed 's/^ *//;s/ *$//')
    [[ -z "$USERNAME" ]] && continue
    PASSWORD="$USERNAME" # per request: username == password in dev
    EMAIL="${USERNAME}@example.com"
    echo "[keycloak-setup] CSV user '${USERNAME}' with roles '${ROLES}'"
    ensure_user "$USERNAME" "$PASSWORD" "$EMAIL" "$USERNAME" "$USERNAME"
    [[ -n "$ROLES" ]] && assign_roles "$USERNAME" "$ROLES"
  done < "$USERS_CSV"
else
  echo "[keycloak-setup] ERROR: USERS_CSV not provided or file not found. CSV is required."
  exit 1
fi

echo "[keycloak-setup] Updating client secret for clientId='${OIDC_CLIENT_ID}' in realm '${REALM}'..."
CLIENT_UUID=$(/opt/keycloak/bin/kcadm.sh get clients -r "${REALM}" -q clientId="${OIDC_CLIENT_ID}" |
  sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
if [[ -n "${CLIENT_UUID}" ]]; then
  /opt/keycloak/bin/kcadm.sh update clients/"${CLIENT_UUID}" -r "${REALM}" -s "secret=${OIDC_CLIENT_SECRET}"
  echo "[keycloak-setup] Client secret updated for ${CLIENT_UUID}."
else
  echo "[keycloak-setup] WARNING: Could not determine client UUID for '${OIDC_CLIENT_ID}'. Skipping secret update."
fi

echo "[keycloak-setup] Done."

touch $SETUP_COMPLETE_FILE_PATH
