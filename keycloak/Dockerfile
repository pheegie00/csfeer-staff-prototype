# Keycloak for the CORE prototype deploy.
#
# - Uses Keycloak 26.x's bitnami-style "start-dev" mode (no HTTPS cert
#   needed; Fly's edge handles TLS).
# - Bakes the realm import into /opt/keycloak/data/import so a fresh
#   machine boots with our csfeer realm + 10 demo users already in place.
# - Persists realm state via H2 (file-backed) at /opt/keycloak/data/h2/.
#   For a prototype this is fine; if the machine is destroyed, the next
#   boot re-imports from the JSON.

FROM quay.io/keycloak/keycloak:26.4

# Enable the health endpoint so Fly's TCP check has something solid to hit.
ENV KC_HEALTH_ENABLED=true \
    KC_METRICS_ENABLED=false \
    KC_HTTP_ENABLED=true \
    KC_HOSTNAME_STRICT=false \
    KC_HOSTNAME_STRICT_HTTPS=false \
    KC_PROXY_HEADERS=xforwarded \
    KC_LOG_LEVEL=INFO

# Realm import. Keycloak picks up everything in /opt/keycloak/data/import/
# on first boot via the --import-realm flag passed in CMD below.
COPY --chown=1000:0 realm-import.json /opt/keycloak/data/import/realm-import.json

EXPOSE 8080

# `start-dev` runs Keycloak with development defaults (HTTP, in-memory
# cache, lenient hostname checks). Fine for a prototype demo.
# --import-realm tells Keycloak to import any JSON in /opt/keycloak/data/import/
# on startup. Idempotent: if the realm already exists, the import is skipped.
CMD ["start-dev", "--import-realm"]
