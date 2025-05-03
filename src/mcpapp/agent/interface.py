from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .action import AgentActionProtocol


class DisplayInterface(ABC):
    @abstractmethod
    def display(self, chunk: "AgentActionProtocol"):
        ...

    @abstractmethod
    def display_text_response(self, text: str):
        ...

    def display_tool_use(self, name: str, tool_input: dict[str, str]):
        raise NotImplementedError("This UI does not support tool use display.")

    def display_image_response(self, image_data: bytes):
        raise NotImplementedError("This UI does not support image display.")
