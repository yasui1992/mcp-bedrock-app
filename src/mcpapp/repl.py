from typing import TYPE_CHECKING

from prompt_toolkit import PromptSession

from .agent import BedrockAgent, DisplayInterface
from .agent.action import TextResponseAction, ToolUseAction

if TYPE_CHECKING:
    from .agent.action import AgentActionProtocol


class ExitREPL(Exception):
    """Raised to signal that the REPL should exit."""
    pass


class REPL(DisplayInterface):
    def __init__(self, agent: BedrockAgent):
        self.agent = agent

    async def arun(self):
        session: PromptSession = PromptSession()
        print("Welcome to the mcp-bedrock-app.")
        print("Type 'exit' or press Ctrl+C / Ctrl+D to quit.")

        while True:
            try:
                text = await session.prompt_async("> ")
                await self._handle_input_text(text)
            except (KeyboardInterrupt, EOFError, ExitREPL):
                break
            except Exception:
                raise

    async def _handle_input_text(self, text: str):
        if len(text) == 0:
            pass
        elif text == "exit":
            raise ExitREPL("Typed 'exit'.")
        else:
            results = self.agent.ainvoke(text)
            async for chunk in results:
                self.display(chunk)

    def display(self, chunk: "AgentActionProtocol"):
        if isinstance(chunk, TextResponseAction):
            self.display_text_response(chunk.text)
        elif isinstance(chunk, ToolUseAction):
            self.display_tool_use(chunk.name, chunk.tool_input)

    def display_text_response(self, text: str):
        print(text)

    def display_tool_use(
        self,
        name: str,
        tool_input: dict[str, str]
    ):
        print("==== ToolUse ====")
        print(f"name: {name}")
        print(f"input: {tool_input}")
        print("=================")
