.PHONY: build start start-local stop restart reset-all reset-db \
        test-unit test-unit-ci test-e2e test-e2e-ci \
        native-migrate native-load-form native-nuke-forms native-create-erds \
        native-test-unit native-test-e2e native-test-e2e-headed native-test-e2e-debug \
        native-test-e2e-webkit native-test-e2e-auth

UV   := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:/usr/bin:$(PATH)
IMAGE_NAME ?=
CI_COMPOSE = IMAGE_NAME=$${IMAGE_NAME} docker compose -f devops/docker/docker-compose-ci.yml
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

# Usage: make test-unit [TEST=tests/unit/form_manager/test_fields.py::test_name]
test-unit:
	docker compose run --rm app uv run pytest $${TEST:-tests/unit} -v

test-unit-ci:
	$(CI_COMPOSE) run --rm app uv run pytest $${TEST:-tests/unit} -v

# Usage: make test-e2e [TEST=tests/e2e/test_form_manager.py::test_name]
test-e2e:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	docker compose run --rm e2e uv run pytest $${TEST:-tests/e2e/} -v -m e2e

test-e2e-ci:
	@echo "Starting services..."
	$(CI_COMPOSE) up -d --remove-orphans
	@echo "Loading seed data..."
	$(CI_COMPOSE) exec app uv run manage.py migrate
	$(CI_COMPOSE) exec app uv run manage.py seed_demo_org --all
	$(CI_COMPOSE) exec app uv run manage.py load_initial_forms
	@echo "Running tests ..."
	$(CI_COMPOSE) exec app uv run pytest $${TEST:-tests/e2e/} -v -m e2e -s
	@echo "Tearing down containers."
	$(CI_COMPOSE) down

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
