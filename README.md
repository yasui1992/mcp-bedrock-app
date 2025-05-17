# mcp-bedrock-app

This project is for personal practice and learning.

## Environment

- Architecture: x86_64
- OS: Ubuntu 24.04.2 LTS  
  (Confirmed on Ubuntu 24.04.2 LTS. May also work on most Linux distributions.)
- Required tools:
  - make
  - Docker

## Preparation

### Environment variables
To configure the necessary environment variables for AWS and Bedrock:

1. Set up AWS credentials (with an IAM role that has access to the Bedrock Converse API).
2. Set the Bedrock model ID.

Run the following command to create or update your `.env` file:

```sh
cat <<EOF > .env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=ap-northeast-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
EOF
```

### Set up mcp_servers.json
You will also need to set up the `mcp_servers.json` file in the same directory as the `README.md` file. 
It is used to configure the MCP server settings.
The file is excluded from Git version control by `.gitignore`, so you can customize it as needed.

For example, create the `mcp_servers.json` file with the following contents:

```.json
{
    "mcpServers": {
        "aws-documentation": {
            "command": "uvx",
            "args": [
                "awslabs.aws-documentation-mcp-server@latest"
            ],
            "env": {
                "FASTMCP_LOG_LEVEL": "ERROR"
            }
        }
    }
}
```

## Usage
To start the application, run:

```sh
make up
```

If you want to enable debugging, run:

```sh
make up-debug
```

To start the development environment with live code updates, run:

```sh
make up-dev
```

If you want to enable debugging in the development environment, run:

```sh
make up-dev-debug
```

## Testing

To run the tests, use:

```sh
make test
```

## Recent Changes

### Multiple Tool Results Preservation

The application now properly preserves all tool results in the conversation history when multiple tools are returned from a single Bedrock ConverseAPI call. Previously, only the last tool result was being preserved in the history.

This change ensures that when the LLM suggests multiple tools in a single response, all tool results are included in the conversation context for subsequent interactions, leading to more coherent and contextually aware responses.

