from typing import AsyncGenerator
import json
import logging
from typing import Final

import boto3
from mcp import ClientSession, Tool
import more_itertools as miter
from mypy_boto3_bedrock_runtime.type_defs import MessageTypeDef


logger = logging.getLogger("mcpapp.agent")


class BedrockAgent:
    # TODO: Resolve hard-coding
    BEDROCK_MODEL_ID: Final[str] = "anthropic.claude-3-haiku-20240307-v1:0"

    def __init__(
        self,
        mcp_session: ClientSession,
        max_actions: int = 10
    ):
        self.mcp_session = mcp_session
        self.max_actions = max_actions

        self._llm_client = boto3.client("bedrock-runtime")
        self._tools: list[Tool] = []

    async def afetch_tools(self):
        result = await self.mcp_session.list_tools()
        logger.debug(result.model_dump_json())

        self._tools = result.tools

    async def ainvoke(self, text: str) -> AsyncGenerator[str, None]:
        is_end = False
        messages: list[MessageTypeDef] = [
            {"role": "user", "content": [ { "text": text } ]}
        ]

        for _ in range(self.max_actions):
            converse_response = self._converse(messages)
            stop_reason = converse_response["stopReason"]

            if stop_reason == "tool_use":
                role = converse_response["output"]["message"]["role"]
                content = converse_response["output"]["message"]["content"]

                for item in content:
                    k, v = miter.only(item.items()) 

                    if k == "text":
                        messages.append({
                            "role": role,
                            "content": [item]
                        })
                    elif k == "toolUse":
                        messages.append({
                            "role": role,
                            "content": [item]
                        })

                        tool_response = await self.mcp_session.call_tool(
                            v["name"],
                            v["input"]
                        )
                        logger.debug(tool_response.model_dump_json())

                        messages.append({
                            "role": "user",
                            "content": [{
                                "toolResult": {
                                    "toolUseId": v["toolUseId"],
                                    "content": [{
                                        "json": {
                                            "text": miter.only(tool_response.content).text  # noqa: E501
                                        }
                                    }]
                                }
                            }]
                        })

            else:
                yield miter.only(converse_response["output"]["message"]["content"])["text"]  # noqa: E501
                is_end = True

            if is_end:
                break

    def _converse(self, messages: list[MessageTypeDef]):
        logger.debug(json.dumps(messages, ensure_ascii=False))

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
        logger.debug(json.dumps(response, ensure_ascii=False))

        return response
