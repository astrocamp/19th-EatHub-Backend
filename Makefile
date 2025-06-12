# Makefile - for Docker Compose Prod Deployment

# === 參數設定 ===
ifeq ($(env),prod)
	COMPOSE_FILE := docker-compose.prod.yml
	ENV_FILE := .env
else
	COMPOSE_FILE ?= docker-compose.local.yml
	ENV_FILE ?= .env
endif
PROJECT_DIR=$(shell pwd)
DOCKER_COMPOSE=docker-compose --env-file $(PROJECT_DIR)/$(ENV_FILE) -f $(COMPOSE_FILE)

# === 指令 ===

.PHONY: up down restart build logs ps

## 啟動服務（背景模式）
up:
	$(DOCKER_COMPOSE) up -d

## 停止服務
down:
	$(DOCKER_COMPOSE) down

## 更新版本，重新啟動服務（包含 build）
restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d --build

## 僅 build（不啟動）
build:
	$(DOCKER_COMPOSE) build

## 顯示日誌
logs:
	$(DOCKER_COMPOSE) logs -f

## 顯示容器狀態
ps:
	$(DOCKER_COMPOSE) ps
