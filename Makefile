.PHONY: create-erds down down-all rm-volume restart restart-fresh oauth-setup test-e2e test-e2e-headed test-e2e-debug test-e2e-webkit install-beads

UV := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)

create-erds:
	$(UV) run python manage.py generate_er_diagram

migrate:
	$(UV) run python manage.py migrate

load-form:
	$(UV) run python manage.py load_initial_forms

nuke-forms:
	$(UV) run python manage.py nuke_forms

build:
	docker compose build

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

test-unit:
	$(UV) run pytest tests/unit -v

test-unit-with-docker:
	docker exec -it csfeer-app-1 bash -c "make test-unit"

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

test-e2e-webkit:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	@echo "Running tests with WebKit (for macOS Sequoia compatibility)..."
	$(UV) run pytest tests/e2e/ -v -m e2e --headed --browser=webkit --slowmo 1000

test-e2e-auth:
	@echo "Starting services..."
	@docker compose up -d app
	@echo "Waiting for app to be ready..."
	@sleep 5
	$(UV) run pytest tests/e2e/ -v -m "e2e and auth"

configure-beads:
	@bd init --prefix bd --server-port 3307 --force
	@bd config set jira.url "https://jira.acf.gov"
	@bd config set jira.project "FE"
	@bd config set allowed_prefixes "FE"
	@bd config set jira.status_map.review "Review"
	@bd config set jira.status_map.testing "Testing"
	@bd config set jira.api_version 2
	@echo "Beads has been configured, but you need to set your personal jira access token. Run the following command with your token: "
	@echo "bd config set  jira.api_token \"<your jira personal access token>\""

install-beads:
	rm -rf /tmp/beads
	git clone git@github.com:ryanbagwell/beads.git --branch feat/change-jira-status /tmp/beads
	cd /tmp/beads && go build -o bd ./cmd/bd
	mv /tmp/beads/bd ~/.local/bin/bd
	rm -rf /tmp/beads

