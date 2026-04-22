.PHONY: help build start start-local stop restart reset-all reset-db \
        test-unit test-unit-ci test-e2e test-e2e-ci \
        native-migrate native-load-form native-nuke-forms native-create-erds \
        native-test-unit native-test-e2e native-test-e2e-headed native-test-e2e-debug \
        native-test-e2e-webkit native-test-e2e-auth

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-30s %s\n", $$1, $$2}'

UV   := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:/usr/bin:$(PATH)
IMAGE_NAME ?=
CI_COMPOSE = IMAGE_NAME=$${IMAGE_NAME} docker compose -f devops/docker/docker-compose-ci.yml
TEST ?=

# ── Docker ────────────────────────────────────────────────────────────────────

build: ## Build Docker images
	docker compose build

start: ## Start all services
	docker compose up -d

# Start only db and mock-oauth (run the app locally via uv or VSCode launch config)
start-local: ## Start only storage, db and mock-oauth for local development
	docker compose up -d db mock-oauth storage

stop: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose down && docker compose up -d

reset-all: ## Stop services and remove all volumes
	docker compose down --volumes

reset-db: ## Remove the postgres data volume
	- docker volume rm csfeer_pgdata

# Usage: make test-unit [TEST=tests/unit/form_manager/test_fields.py::test_name]
test-unit: ## Run unit tests (TEST=path optional)
	docker compose run --rm app uv run pytest $${TEST:-tests/unit} -v

setup-tests-ci: ## Set up CI services and seed data
	@echo "Starting services..."
	$(CI_COMPOSE) down -v
	$(CI_COMPOSE) up -d
	$(CI_COMPOSE) exec app uv run manage.py migrate --noinput
	@echo "Loading seed data..."
	$(CI_COMPOSE) exec app uv run manage.py seed_e2e_users
	$(CI_COMPOSE) exec app uv run manage.py seed_demo_org --all
	$(CI_COMPOSE) exec app uv run manage.py load_initial_forms

test-unit-ci: ## Run unit tests in CI (TEST=path optional)
	$(CI_COMPOSE) exec app uv run pytest $${TEST:-tests/unit} -v

# Usage: make test-e2e [TEST=tests/e2e/test_form_manager.py::test_name]
test-e2e: ## Run e2e tests (TEST=path optional)
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	docker compose exec app uv run pytest $${TEST:-tests/e2e/} -v -m e2e

test-e2e-ci: ## Run e2e tests in CI (TEST=path optional)
	$(CI_COMPOSE) exec app uv run pytest $${TEST:-tests/e2e/} -v -m e2e -s --screenshot=off --video=off

# ── Native (host) ─────────────────────────────────────────────────────────────

native-migrate: ## Run database migrations (native)
	$(UV) run python manage.py migrate

native-load-form: ## Load initial forms (native)
	$(UV) run python manage.py load_initial_forms

native-nuke-forms: ## Delete all forms (native)
	$(UV) run python manage.py nuke_forms

native-create-erds: ## Generate ER diagrams (native)
	$(UV) run python manage.py generate_er_diagram

native-test-unit: ## Run unit tests natively (TEST=path optional)
	$(UV) run pytest $${TEST:-tests/unit} -v

_start-services:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5

# Usage: make native-test-e2e [TEST=tests/e2e/test_form_manager.py::test_name]
native-test-e2e: _start-services ## Run e2e tests natively (TEST=path optional)
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e

native-test-e2e-headed: _start-services ## Run e2e tests natively with browser visible
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed

native-test-e2e-debug: _start-services ## Run e2e tests natively in debug mode (slow)
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed --slowmo 1000

# Use WebKit for macOS Sequoia compatibility
native-test-e2e-webkit: _start-services ## Run e2e tests natively with WebKit (macOS Sequoia)
	$(UV) run pytest $${TEST:-tests/e2e/} -v -m e2e --headed --browser=webkit --slowmo 1000

native-test-e2e-auth: _start-services ## Run auth e2e tests natively
	$(UV) run pytest tests/e2e/ -v -m "e2e and auth"
