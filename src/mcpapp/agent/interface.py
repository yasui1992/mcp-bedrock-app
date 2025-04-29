from abc import abstractmethod
from typing import Protocol


class DisplayInterface(Protocol):
    @abstractmethod
    def display_text_response(self, text: str):
        ...

    @abstractmethod
    def display_tool_use(self, name: str, tool_input: dict[str, str]):
        ...
