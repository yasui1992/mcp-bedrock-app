from typing import Protocol

from mypy_boto3_bedrock_runtime.type_defs import (
    ContentBlockOutputTypeDef,
    ContentBlockTypeDef,
    MessageTypeDef
)


class MessageProtocol(Protocol):
    def to_bedrock_conversion(self) -> MessageTypeDef:
        ...


class UserMessage:
    def __init__(
        self,
        contents: list[ContentBlockTypeDef]
    ):
        self.contents = contents

    def to_bedrock_conversion(self) -> MessageTypeDef:
        return {
            "role": "user",
            "content": self.contents
        }


class AssistantMessage:
    def __init__(
        self,
        contents: list[ContentBlockOutputTypeDef]
    ):
        self.contents = contents

    def to_bedrock_conversion(self) -> MessageTypeDef:
        return {
            "role": "assistant",
            "content": self.contents
        }
