# Makefile - Docker Compose

ifeq ($(env),prod)
	COMPOSE_FILE := docker-compose.prod.yml
	ENV_FILE := .env
else
	COMPOSE_FILE ?= docker-compose.local.yml
	ENV_FILE ?= .env
endif

PROJECT_DIR := $(shell pwd)
DOCKER_COMPOSE := docker compose --env-file $(PROJECT_DIR)/$(ENV_FILE) -f $(COMPOSE_FILE)


.PHONY: up down restart build logs ps test migrate createsuperuser collectstatic

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d --build

build:
	$(DOCKER_COMPOSE) build

logs:
	$(DOCKER_COMPOSE) logs -f

ps:
	$(DOCKER_COMPOSE) ps

test:
	docker compose -f docker-compose.local.yml exec web pytest

migrate:
	$(DOCKER_COMPOSE) exec web python manage.py migrate

createsuperuser:
	$(DOCKER_COMPOSE) exec web python manage.py createsuperuser

collectstatic:
	$(DOCKER_COMPOSE) exec web python manage.py collectstatic --noinput
