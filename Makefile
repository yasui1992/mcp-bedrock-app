build:
	docker build \
	--platform linux/x86_64 \
	--target prod \
	-t mcp-bedrock-client \
	.


build-dev:
	docker build \
	--platform linux/x86_64 \
	--target dev \
	-t mcp-bedrock-client:dev \
	.

run:
	docker run \
	--name mcp-bedrock-client \
	--env-file .env \
	--rm \
	-it \
	mcp-bedrock-client

run-debug:
	docker run \
	--name mcp-bedrock-client \
	--env-file .env \
	--rm \
	-e LOG_LEVEL=debug \
	-it \
	mcp-bedrock-client

run-dev:
	docker run \
	--name mcp-bedrock-client-dev \
	--env-file .env \
	--rm \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-d \
	mcp-bedrock-client:dev \
	tail -f /dev/null

run-dev-debug:
	docker run \
	--name mcp-bedrock-client-dev \
	--env-file .env \
	--rm \
	-e LOG_LEVEL=debug \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-d \
	mcp-bedrock-client:dev \
	tail -f /dev/null


run-ruff:
	@docker run \
	--rm \
	-i \
	mcp-bedrock-client:dev \
	ruff check .

run-mypy:
	@docker run \
	--rm \
	-i \
	mcp-bedrock-client:dev \
	mypy .

up: build run

up-debug: build run-debug

up-dev: build-dev run-dev

up-dev-debug: build-dev run-dev-debug

up-check: build-dev run-ruff run-mypy

down-dev:
	docker rm -f mcp-bedrock-client-dev
