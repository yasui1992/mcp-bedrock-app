from typing import AsyncGenerator
import json
import logging
from typing import Final

import boto3
from mcp import ClientSession, Tool
from mypy_boto3_bedrock_runtime.type_defs import MessageTypeDef


logger = logging.getLogger("mcpapp.agent")


class BedrockAgent:
    # TODO: Resolve hard-coding
    BEDROCK_MODEL_ID: Final[str] = "anthropic.claude-3-haiku-20240307-v1:0"

    def __init__(self, mcp_session: ClientSession):
        self.mcp_session = mcp_session
        self._llm_client = boto3.client("bedrock-runtime")
        self._tools: list[Tool] = []

    async def afetch_tools(self):
        result = await self.mcp_session.list_tools()
        logger.debug(result.model_dump_json())

        self._tools = result.tools

    async def ainvoke(self, text: str) -> AsyncGenerator[str, None]:
        response = self._converse(text)

        yield response["stopReason"]

    def _converse(self, text: str):
        messages: list[MessageTypeDef] = [
            {"role": "user", "content": [ { "text": text } ]}
        ]

        # TODO: Resolve too deeply nested
        response = self._llm_client.converse(
            modelId=self.BEDROCK_MODEL_ID,
            messages=messages,
            toolConfig={
                "tools": [
                    {
                        "toolSpec": {
                            "name": t.name,
                            "description": t.description or "",
                            "inputSchema": {
                                "json": t.inputSchema
                            }
                        }
                    }
                    for t in self._tools
                ]
            }
        )
        logger.debug(json.dumps(response))

        return response
