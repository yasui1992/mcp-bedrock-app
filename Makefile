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
    -v src:/app/src \
	-it \
	mcp-bedrock-client:dev

up-dev: build-dev run-dev

down-dev:
	docker rm -f mcp-bedrock-client-dev
