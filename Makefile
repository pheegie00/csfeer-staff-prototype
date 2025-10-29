.PHONY: create-erds down down-all rm-volume restart restart-fresh oauth-setup

UV := $(shell which uv || echo $$HOME/.local/bin/uv)
PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)

create-erds:
	$(UV) run python manage.py generate_er_diagram

start:
	docker compose up -d

start-local:
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
