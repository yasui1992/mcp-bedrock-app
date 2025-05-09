import logging

from prompt_toolkit import PromptSession

from .agent import BedrockAgent, DisplayMixin


logger = logging.getLogger(__name__)


class ExitREPL(Exception):
    """Raised to signal that the REPL should exit."""
    pass


class REPL(DisplayMixin):
    def __init__(self, agent: BedrockAgent):
        self.agent = agent

    async def arun(self):
        logger.info("REPL started.")

        session: PromptSession = PromptSession()
        print("Welcome to the mcp-bedrock-app.")
        print("Type 'exit' or press Ctrl+C / Ctrl+D to quit.")

        while True:
            try:
                text = await session.prompt_async("> ")
                await self._handle_input_text(text)
            except (KeyboardInterrupt, EOFError, ExitREPL):
                logger.info("REPL terminated.")
                break
            except Exception:
                logger.exception("Unexpected error occurred. REPL terminated.")
                raise

    async def _handle_input_text(self, text: str):
        logger.debug(f'"text": {text}')
        if len(text) == 0:
            pass
        elif text == "exit":
            raise ExitREPL("Typed 'exit'.")
        else:
            results = self.agent.ainvoke(text)
            async for chunk in results:
                self.display(chunk)

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
