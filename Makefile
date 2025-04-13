build-dev:
	docker build \
	--platform linux/x86_64 \
	--target dev \
	-t mcp-bedrock-client:dev \
	.

run-dev:
	docker run \
	--name mcp-bedrock-client-dev \
	--rm \
	-v ./src:/app/src \
	-v ./pyproject.toml:/app/pyproject.toml \
	-v ./uv.lock:/app/uv.lock \
	-d \
	mcp-bedrock-client:dev \
	tail -f /dev/null

up-dev: build-dev run-dev

down-dev:
	docker rm -f mcp-bedrock-client-dev
