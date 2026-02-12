# FlurPilot Core - Production Operations Makefile

COMPOSE_FILE := docker-compose.prod.yml
PROJECT_NAME := flurpilot

.PHONY: up down logs build pull migrate shell-web shell-worker help preview

preview: ## Build and run locally on http://localhost (Preview Mode)
	@echo "Starting Local Preview on http://localhost..."
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.preview.yml -p $(PROJECT_NAME) up --build -d


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services in detached mode
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d

down: ## Stop all services
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down

restart: ## Restart all services
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) restart

logs: ## Tail logs for all services (use SERVICE=name for specific)
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) logs -f $(SERVICE)

build: ## Rebuild all images
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) build

pull: ## Pull latest images
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) pull

shell-web: ## Access the shell of the web container
	docker exec -it $(PROJECT_NAME)-web-1 /bin/sh

shell-worker: ## Access the shell of the worker container
	docker exec -it $(PROJECT_NAME)-worker-1 /bin/bash

db-shell: ## Access the Postgres database via psql
	docker exec -it $(PROJECT_NAME)-db-1 psql -U postgres

migrate: ## Apply latest migrations (Manual cat to psql)
	@echo "Applying migrations..."
	# This matches files in packages/database/supabase/migrations/
	@for file in packages/database/supabase/migrations/*.sql; do \
		echo "Applying $$file..."; \
		cat $$file | docker exec -i $(PROJECT_NAME)-db-1 psql -U postgres; \
	done
	@echo "Done."
