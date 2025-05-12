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
	-it \
	mcp-bedrock-client:dev

run-dev-debug:
	docker run \
	--name mcp-bedrock-client-dev \
	--env-file .env \
	--rm \
	-e LOG_LEVEL=debug \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-it \
	mcp-bedrock-client:dev

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

run-test:
	@docker run \
	--rm \
	-v ./src:/app/src \
	-v ./tests:/app/tests \
	-v ./pyproject.toml:/app/pyproject.toml \
	-i \
	mcp-bedrock-client:dev \
	python -m pytest -v

up: build run

up-debug: build run-debug

up-dev: build-dev run-dev

up-dev-debug: build-dev run-dev-debug

up-check: build-dev run-ruff run-mypy

test: build-dev run-test
