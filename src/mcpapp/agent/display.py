from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .action import TextResponseAction, ToolUseAction

if TYPE_CHECKING:
    from .action import AgentActionProtocol


class DisplayMixin(ABC):
    def display(self, chunk: "AgentActionProtocol"):
        if isinstance(chunk, TextResponseAction):
            self.display_text_response(chunk.text)
        elif isinstance(chunk, ToolUseAction):
            self.display_tool_use(chunk.name, chunk.tool_input)

    @abstractmethod
    def display_text_response(self, text: str):
        raise NotImplementedError("This UI does not support text display.")

    def display_tool_use(self, name: str, tool_input: dict[str, str]):
        raise NotImplementedError("This UI does not support tool use display.")
