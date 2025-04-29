from typing import cast
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime.type_defs import (
        ContentBlockOutputTypeDef,
        ContentBlockTypeDef,
        MessageTypeDef,
        ToolUseBlockOutputTypeDef
    )


class MessageProtocol(Protocol):
    def to_bedrock_conversion(self) -> "MessageTypeDef":
        ...


class UserMessage:
    def __init__(
        self,
        contents: list["ContentBlockTypeDef"]
    ):
        self.contents = contents

    def to_bedrock_conversion(self) -> "MessageTypeDef":
        return {
            "role": "user",
            "content": self.contents
        }


class AssistantMessage:
    def __init__(
        self,
        contents: list["ContentBlockOutputTypeDef"]
    ):
        self.contents = contents

    def to_bedrock_conversion(self) -> "MessageTypeDef":
        return {
            "role": "assistant",
            "content": self.contents
        }

    def find_tool_uses(self) -> list["ToolUseBlockOutputTypeDef"]:
        tool_uses = []

        for content in self.contents:
            key, value = next(iter(content.items()))
            if key == "toolUse":
                tool_uses.append(cast(
                    "ToolUseBlockOutputTypeDef",
                    value
                ))
            else:
                continue

        return tool_uses
