import logging

from prompt_toolkit import PromptSession

from .agent import BedrockAgent, DisplayInterface


logger = logging.getLogger(__name__)


class REPL(DisplayInterface):
    def __init__(self, agent: BedrockAgent):
        self.agent = agent

    async def arun(self):
        session: PromptSession = PromptSession()

        while True:
            try:
                text = await session.prompt_async("> ")
                await self._handle_input_text(text)
            except (KeyboardInterrupt, EOFError):
                break

    async def _handle_input_text(self, text: str):
        if len(text) > 0:
            results = self.agent.ainvoke(text)
            async for chunk in results:
                chunk.display(self)

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
