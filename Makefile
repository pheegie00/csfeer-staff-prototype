.PHONY: create-erds down down-all rm-volume restart restart-fresh oauth-setup test-e2e test-e2e-headed test-e2e-debug

UV := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)

create-erds:
	$(UV) run python manage.py generate_er_diagram

start:
	docker compose up -d

start-local:
	# Start only the local services (db and mock-oauth) without starting the app.
	# Then run the app locally using uv or VSCode's launch configuration.
	# This is useful for development when you want to run the app locally but
	# still need the database and mock OAuth services running in Docker.
	docker compose up -d db mock-oauth

stop:
	docker compose down

reset-all:
	docker compose down --volumes

reset-db:
	- docker volume rm csfeer_pgdata

restart:
	docker compose down && docker compose up -d

oauth-setup:
	docker compose run --rm oauth-setup

# E2E Testing targets
test-e2e:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	$(UV) run pytest tests/e2e/ -v -m e2e

test-e2e-headed:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	$(UV) run pytest tests/e2e/ -v -m e2e --headed

test-e2e-debug:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	$(UV) run pytest tests/e2e/ -v -m e2e --headed --slowmo 1000

test-e2e-auth:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	$(UV) run pytest tests/e2e/ -v -m "e2e and auth"
