build:
	docker build \
	--platform linux/x86_64 \
	--target prod \
	-t mcp-bedrock-app \
	.


build-dev:
	docker build \
	--platform linux/x86_64 \
	--target dev \
	-t mcp-bedrock-app:dev \
	.

run:
	docker run \
	--name mcp-bedrock-app \
	--env-file .env \
	--rm \
	-it \
	mcp-bedrock-app

run-debug:
	docker run \
	--name mcp-bedrock-app \
	--env-file .env \
	--rm \
	-e LOG_LEVEL=debug \
	-it \
	mcp-bedrock-app

run-dev:
	docker run \
	--name mcp-bedrock-app-dev \
	--env-file .env \
	--rm \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-it \
	mcp-bedrock-app:dev

run-dev-debug:
	docker run \
	--name mcp-bedrock-app-dev \
	--env-file .env \
	--rm \
	-e LOG_LEVEL=debug \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-it \
	mcp-bedrock-app:dev

run-ruff:
	@docker run \
	--rm \
	-i \
	mcp-bedrock-app:dev \
	ruff check .

run-mypy:
	@docker run \
	--rm \
	-i \
	mcp-bedrock-app:dev \
	mypy .

up: build run

up-debug: build run-debug

up-dev: build-dev run-dev

up-dev-debug: build-dev run-dev-debug

up-check: build-dev run-ruff run-mypy
