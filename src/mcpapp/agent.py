import json
import logging
from typing import Final

import boto3
from mcp.types import Tool


logger = logging.getLogger("mcpapp.agent")


class BedrockAgent:
    # TODO: Resolve hard-coding
    BEDROCK_MODEL_ID: Final[str] = "anthropic.claude-3-haiku-20240307-v1:0"

    def __init__(self):
        self._llm_client = boto3.client("bedrock-runtime")
        self._tools = []

    def set_tools(self, tools: list[Tool]):
        self._tools = tools

    def invoke(self, text: str):
        response = self._converse(text)
        
        # NOTE: stopReason print is temporary
        print(response["stopReason"])

    def _converse(self, text: str):
        messages = [
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
                            "description": t.description,
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
