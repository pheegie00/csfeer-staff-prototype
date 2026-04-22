#!/bin/bash
set -e

: "${GITHUB_TOKEN:?GITHUB_TOKEN is required}"
: "${GITHUB_REPO:?GITHUB_REPO is required}"
: "${RUNNER_WORK_DIR:?RUNNER_WORK_DIR is required}"

RUNNER_NAME="${RUNNER_NAME:-$(hostname)}"
RUNNER_LABELS="${RUNNER_LABELS:-self-hosted,ubuntu-24.04,linux,x64}"

# Allow the runner user to access the mounted Docker socket
if [ -S /var/run/docker.sock ]; then
    sudo chmod 666 /var/run/docker.sock
fi

# Ensure the work directory exists and is writable by the runner user
sudo mkdir -p "${RUNNER_WORK_DIR}"
sudo chown -R runner:runner "${RUNNER_WORK_DIR}"

# Re-register if .runner is missing or its workFolder doesn't match RUNNER_WORK_DIR
# (the latter catches restarts after a config change without a full container rebuild)
CONFIGURED_WORK_DIR=$(jq -r '.workFolder // empty' .runner 2>/dev/null || true)
if [ ! -f .runner ] || [ "$CONFIGURED_WORK_DIR" != "${RUNNER_WORK_DIR}" ]; then
    # Get a short-lived registration token from the GitHub API
    REG_TOKEN=$(curl -sf -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/${GITHUB_REPO}/actions/runners/registration-token" \
        | jq -r .token)

    if [ -z "$REG_TOKEN" ] || [ "$REG_TOKEN" = "null" ]; then
        echo "ERROR: Failed to obtain registration token. Verify GITHUB_TOKEN has 'repo' scope." >&2
        exit 1
    fi

    ./config.sh \
        --url "https://github.com/${GITHUB_REPO}" \
        --token "${REG_TOKEN}" \
        --name "${RUNNER_NAME}" \
        --labels "${RUNNER_LABELS}" \
        --work "${RUNNER_WORK_DIR}" \
        --unattended \
        --replace \
        --disableupdate
fi

# Deregister cleanly when the container stops
cleanup() {
    echo "Deregistering runner '${RUNNER_NAME}'..."
    REG_TOKEN=$(curl -sf -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/${GITHUB_REPO}/actions/runners/registration-token" \
        | jq -r .token) || true
    ./config.sh remove --token "${REG_TOKEN}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

./run.sh &
RUNNER_PID=$!
wait $RUNNER_PID
