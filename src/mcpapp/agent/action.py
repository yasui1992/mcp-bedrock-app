from abc import abstractmethod
from typing import Protocol, Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime.type_defs import (
        ToolUseBlockOutputTypeDef
    )

    from .interface import DisplayInterface


class AgentActionProtocol(Protocol):
    @abstractmethod
    def display(self, ui: "DisplayInterface"):
        ...


class TextResponseAction:
    def __init__(self, text: str):
        self.text = text

    def display(self, ui: "DisplayInterface"):
        ui.display_text_response(self.text)


class ToolUseAction:
    def __init__(self, name: str, tool_input: dict[str, str]):
        self.name = name
        self.tool_input = tool_input

    def display(self, ui: "DisplayInterface"):
        ui.display_tool_use(self.name, self.tool_input)

    @classmethod
    def from_bedrock_block(cls, tool_use: "ToolUseBlockOutputTypeDef") -> Self:
        return cls(
            name=tool_use["name"],
            tool_input=tool_use["input"]
        )
