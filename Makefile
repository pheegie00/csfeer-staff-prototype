.PHONY: build start start-local stop restart reset-all reset-db oauth-setup \
        test-unit test-e2e \
        native-migrate native-load-form native-nuke-forms native-create-erds \
        native-test-unit native-test-e2e native-test-e2e-headed native-test-e2e-debug \
        native-test-e2e-webkit native-test-e2e-auth \
        configure-beads install-beads

UV   := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:/usr/bin:$(PATH)
DOCKER_COMPOSE_FILE ?=
TEST ?=

# ── Docker ────────────────────────────────────────────────────────────────────

build:
	docker compose build

start:
	docker compose up -d

# Start only db and mock-oauth (run the app locally via uv or VSCode launch config)
start-local:
	docker compose up -d db mock-oauth

stop:
	docker compose down

restart:
	docker compose down && docker compose up -d

reset-all:
	docker compose down --volumes

reset-db:
	- docker volume rm csfeer_pgdata

oauth-setup:
	docker compose run --rm oauth-setup

# Usage: make test-unit [TEST=tests/unit/form_manager/test_fields.py::test_name]
test-unit:
	docker compose -f $${DOCKER_COMPOSE_FILE:-compose.yml} run --rm app uv run pytest $${TEST:-tests/unit} -v

# Usage: make test-e2e [TEST=tests/e2e/test_form_manager.py::test_name]
test-e2e:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	docker compose run --rm e2e uv run pytest $${TEST:-tests/e2e/} -v -m e2e

# ── Native (host) ─────────────────────────────────────────────────────────────

native-migrate:
	$(UV) run python manage.py migrate

native-load-form:
	$(UV) run python manage.py load_initial_forms

native-nuke-forms:
	$(UV) run python manage.py nuke_forms

native-create-erds:
	$(UV) run python manage.py generate_er_diagram

native-test-unit:
	$(UV) run pytest $${TEST:-tests/unit} -v

_start-services:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5

# Usage: make native-test-e2e [TEST=tests/e2e/test_form_manager.py::test_name]
native-test-e2e: _start-services
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e

native-test-e2e-headed: _start-services
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed

native-test-e2e-debug: _start-services
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed --slowmo 1000

# Use WebKit for macOS Sequoia compatibility
native-test-e2e-webkit: _start-services
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed --browser=webkit --slowmo 1000

native-test-e2e-auth: _start-services
	$(UV) run pytest tests/e2e/ -v -m "e2e and auth"

# ── Tooling ───────────────────────────────────────────────────────────────────

configure-beads:
	@bd init --prefix bd --server-port 3307 --force
	@bd config set jira.url "https://jira.acf.gov"
	@bd config set jira.project "FE"
	@bd config set allowed_prefixes "FE"
	@bd config set jira.status_map.review "Review"
	@bd config set jira.status_map.testing "Testing"
	@bd config set jira.api_version 2
	@echo "Beads configured. Set your Jira token with:"
	@echo "  bd config set jira.api_token \"<your token>\""
	@jira-beads-sync configure

install-beads:
	rm -rf /tmp/beads /tmp/jira-beads-sync
	git clone git@github.com:ryanbagwell/beads.git --branch feat/change-jira-status /tmp/beads
	cd /tmp/beads && go build -o bd ./cmd/bd
	mv /tmp/beads/bd ~/.local/bin/bd
	rm -rf /tmp/beads
	git clone --depth 1 --revision 08a02a7bce125a0545ced2f45f594ac8a4b53b71 git@github.com:ryanbagwell/jira-beads-sync.git /tmp/jira-beads-sync
	cd /tmp/jira-beads-sync && go build -o jira-beads-sync ./cmd/jira-beads-sync
	mv /tmp/jira-beads-sync/jira-beads-sync ~/.local/bin/jira-beads-sync
	rm -rf /tmp/jira-beads-sync
	@echo "Beads and jira-beads-sync installed."
