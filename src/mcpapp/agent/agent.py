from typing import AsyncGenerator
from typing import cast
from typing import TYPE_CHECKING
import json
import logging
import os

from mcp import ClientSession
from mcp.types import TextContent

from .tool_config import ToolConfig
from .action import (
    TextResponseAction,
    ToolUseAction
)
from .message import (
    AssistantMessage,
    UserMessage
)

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.literals import StopReasonType
    from mypy_boto3_bedrock_runtime.type_defs import (
        ToolUseBlockOutputTypeDef,
        ToolResultBlockOutputTypeDef,
        ToolResultContentBlockOutputTypeDef
    )

    from .action import AgentActionProtocol
    from .message import MessageProtocol


logger = logging.getLogger(__name__)

BEDROCK_MODEL_ID = os.environ["BEDROCK_MODEL_ID"]
SYSTEM_PROMPT = """\
You are a helpful assistant. To answer user queries:

- Use tools to gather information when needed.
- Refine your answer using the tool results.
- Call more tools if necessary.

When you use information from documents, include the document title, URL,
and a reference section in your response. The reference section should be
clearly marked as "Reference:" and placed at the end of your answer.
"""


class BedrockAgent:
    def __init__(
        self,
        mcp_session: ClientSession,
        llm_client: "BedrockRuntimeClient",
        max_actions: int = 10
    ):
        self.mcp_session = mcp_session
        self.llm_client = llm_client
        self.max_actions = max_actions

        self._tool_config = ToolConfig()

    async def afetch_tools(self):
        result = await self.mcp_session.list_tools()
        logger.debug(result.model_dump_json())

        self._tool_config.set_tools(result.tools)

    async def ainvoke(self, text: str) -> AsyncGenerator["AgentActionProtocol", None]:
        is_end = False
        original_user_msg = UserMessage([{"text": text}])

        assistant_msg: AssistantMessage | None = None
        tool_result_msg: UserMessage | None = None

        for _ in range(self.max_actions):
            messages: list["MessageProtocol"] = [original_user_msg]
            if assistant_msg is not None:
                messages.append(assistant_msg)
            if tool_result_msg is not None:
                messages.append(tool_result_msg)

            assistant_msg, stop_reason = self._call_bedrock_converse(messages)

            if stop_reason == "tool_use":
                for tool_use_block in assistant_msg.find_tool_uses():
                    yield ToolUseAction.from_bedrock_block(tool_use_block)

                    tool_result = await self._acall_tool(tool_use_block)
                    tool_result_msg = UserMessage([{"toolResult": tool_result}])

            elif stop_reason == "end_turn":
                assert len(assistant_msg.contents) == 1
                yield TextResponseAction(assistant_msg.contents[0]["text"])

                is_end = True
            else:
                raise ValueError(f"Unsupported stop_reason: {stop_reason}")

            if is_end:
                break

    async def _acall_tool(
        self,
        tool_use_block: "ToolUseBlockOutputTypeDef"
    ) -> "ToolResultBlockOutputTypeDef":

        tool_response = await self.mcp_session.call_tool(
            tool_use_block["name"],
            tool_use_block["input"]
        )
        logger.debug(f"Tool response: {tool_response.model_dump_json()}")

        contents = []
        for cnt in tool_response.content:
            assert isinstance(cnt, TextContent)

            contents.append(cast(
                "ToolResultContentBlockOutputTypeDef",
                {"text": cnt.text}
            ))

        return {
            "toolUseId": tool_use_block["toolUseId"],
            "content": contents
        }

    def _call_bedrock_converse(
        self,
        messages: list["MessageProtocol"]
    ) -> tuple[AssistantMessage, "StopReasonType"]:
        bedrock_conversion_messages = [
            msg.to_bedrock_conversion()
            for msg in messages
        ]
        logger.debug(json.dumps(bedrock_conversion_messages, ensure_ascii=False))

        tool_config = self._tool_config.dump_to_converse_dict()

        response = self.llm_client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=bedrock_conversion_messages,
            toolConfig=tool_config,
            system=[{"text": SYSTEM_PROMPT}]
        )
        logger.debug(json.dumps(response, ensure_ascii=False))

        assert response["output"]["message"]["role"] == "assistant"

        output_message = AssistantMessage(response["output"]["message"]["content"])
        stop_reason = response["stopReason"]

        return output_message, stop_reason
