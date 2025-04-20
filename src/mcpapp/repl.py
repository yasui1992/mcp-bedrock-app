import logging

from prompt_toolkit import PromptSession

from mcpapp.agent import BedrockAgent


logger = logging.getLogger("mcpapp.repl")


# TODO: Create an interface protocol to support other IFs (e.g., REST API)
class REPL:
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
                print(chunk)
