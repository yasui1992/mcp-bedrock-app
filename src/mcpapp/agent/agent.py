from typing import AsyncGenerator
import json
import logging
import os

import boto3
from mcp import ClientSession
from mcp.types import TextContent
from mypy_boto3_bedrock_runtime.literals import StopReasonType
from mypy_boto3_bedrock_runtime.type_defs import (
    ToolUseBlockOutputTypeDef,
    ToolResultBlockOutputTypeDef
)

from mcpapp.agent.tool_config import ToolConfig
from mcpapp.agent.message import (
    MessageProtocol,
    AssistantMessage,
    UserMessage
)


logger = logging.getLogger(__name__)

BEDROCK_MODEL_ID = os.environ["BEDROCK_MODEL_ID"]


class BedrockAgent:
    def __init__(
        self,
        mcp_session: ClientSession,
        max_actions: int = 10
    ):
        self.mcp_session = mcp_session
        self.max_actions = max_actions

        self._llm_client = boto3.client("bedrock-runtime")
        self._tool_config = ToolConfig()

    async def afetch_tools(self):
        result = await self.mcp_session.list_tools()
        logger.debug(result.model_dump_json())

        self._tool_config.set_tools(result.tools)

    async def ainvoke(self, text: str) -> AsyncGenerator[str, None]:
        is_end = False
        messages: list[MessageProtocol] = [
            UserMessage([{"text": text}])
        ]

        for _ in range(self.max_actions):
            assistant_msg, stop_reason = self._call_bedrock_converse(messages)
            messages.append(assistant_msg)

            if stop_reason == "tool_use":
                for tool_use_block in assistant_msg.find_tool_uses():
                    yield "==== ToolUse ===="
                    yield "name: {}".format(tool_use_block["name"])
                    yield "input: {}".format(tool_use_block["input"])
                    yield "================="

                    tool_result = await self._acall_tool(tool_use_block)

                    tool_result_msg = UserMessage([{"toolResult": tool_result}])
                    messages.append(tool_result_msg)

            elif stop_reason == "end_turn":
                assert len(assistant_msg.contents) == 1
                yield assistant_msg.contents[0]["text"]
                is_end = True
            else:
                raise ValueError(f"Unsupported stop_reason: {stop_reason}")
            if is_end:
                break

    async def _acall_tool(
        self,
        tool_use_block: ToolUseBlockOutputTypeDef
    ) -> ToolResultBlockOutputTypeDef:

        tool_response = await self.mcp_session.call_tool(
            tool_use_block["name"],
            tool_use_block["input"]
        )
        logger.debug(f"Tool response: {tool_response.model_dump_json()}")

        if len(tool_response.content) > 1:
            num_contents = len(tool_response.content)
            raise ValueError(f"Expected exactly one content item, got: {num_contents}.")

        content_item = tool_response.content[0]
        assert isinstance(content_item, TextContent)

        return {
            "toolUseId": tool_use_block["toolUseId"],
            "content": [{
                "json": {
                    "text": content_item.text
                }
            }]
        }

    def _call_bedrock_converse(
        self,
        messages: list[MessageProtocol]
    ) -> tuple[AssistantMessage, StopReasonType]:
        bedrock_conversion_messages = [
            msg.to_bedrock_conversion()
            for msg in messages
        ]
        logger.debug(json.dumps(bedrock_conversion_messages, ensure_ascii=False))

        tool_config = self._tool_config.dump_to_converse_dict()

        response = self._llm_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=bedrock_conversion_messages,
            toolConfig=tool_config
        )
        logger.debug(json.dumps(response, ensure_ascii=False))

        assert response["output"]["message"]["role"] == "assistant"

        output_message = AssistantMessage(response["output"]["message"]["content"])
        stop_reason = response["stopReason"]

        return output_message, stop_reason
