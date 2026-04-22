# Self-Hosted GitHub Actions Runner

A Docker-based GitHub Actions runner that mimics the `ubuntu-latest` environment (Ubuntu 24.04). Runs on macOS via Docker Desktop using `linux/amd64` emulation.

## Pre-installed tools

| Tool | Version |
|------|---------|
| Ubuntu | 24.04 |
| Python | 3.12 |
| Node.js | 22 LTS |
| Go | 1.24 |
| Java (JDK) | 17 |
| Docker CLI | latest |
| GitHub CLI (`gh`) | latest |
| Git, make, cmake, gcc, curl, wget, jq, zip | system |

## Prerequisites

- [Docker or Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) running
- A GitHub personal access token with **`repo` scope** — create one at GitHub → Settings → Developer settings → Personal access tokens (classic)

## Setup

**1. Create your `.env` file**

```bash
cp .env.example .env
```

Edit `.env` and fill in all values:

```dotenv
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=focusconsulting/csfeer
RUNNER_NAME=<YOUR RUNNER NAME>
RUNNER_LABELS=self-hosted,ubuntu-latest,linux,x64
RUNNER_WORK_DIR=/tmp/runner-work
```

`RUNNER_WORK_DIR` must be an absolute host path under a directory Docker Desktop already shares (e.g. `/tmp`, `/Users`). It is mounted at the same path inside the container so that nested `docker run -v` mounts work correctly.

**2. Build and start**

```bash
docker compose up --build -d
```

The first build takes several minutes — it downloads Node, Go, Java, the Docker CLI, and the runner binary.

**3. Verify**

The runner should appear as **Idle** at:
`https://github.com/focusconsulting/csfeer/settings/actions/runners`

## Using the runner in a workflow

```yaml
jobs:
  build:
    runs-on: [self-hosted, ubuntu-latest]
```

## Day-to-day operations

| Task | Command |
|------|---------|
| Start | `docker compose up -d` |
| Stop (deregisters runner) | `docker compose down` |
| View logs | `docker compose logs -f` |
| Rebuild after config changes | `docker compose up --build -d` |

> **Note:** `docker compose restart` keeps the container alive without recreating it. The entrypoint detects stale configuration (e.g. a changed `RUNNER_WORK_DIR`) and re-registers automatically on next start, but changes to `entrypoint.sh` or `Dockerfile` require `--build`.

## How it works

- The runner registers with GitHub on startup using a short-lived token fetched via the API. It deregisters cleanly when the container stops.
- Re-registration is skipped if `.runner` already exists **and** its `workFolder` matches `RUNNER_WORK_DIR`. This avoids consuming a registration token on every restart.
- The host Docker socket (`/var/run/docker.sock`) is mounted into the container so workflows can run `docker` commands against the host daemon.
- `restart: unless-stopped` keeps the runner alive across Docker Desktop restarts and crashes.
