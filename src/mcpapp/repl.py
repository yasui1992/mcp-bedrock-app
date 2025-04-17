import logging

from prompt_toolkit import PromptSession

from mcpapp.client import MCPClient
from mcpapp.agent import BedrockAgent


logger = logging.getLogger("mcpapp.repl")


# TODO: Create an interface protocol to support other IFs (e.g., REST API)
class REPL:
    def __init__(self, agent: BedrockAgent):
        self.agent = agent

    async def aset_mcp_client(self, mcp_client: MCPClient):
        async with mcp_client.aconnent_session() as mcp_session:
            result = await mcp_session.list_tools()
            logger.debug(result.model_dump_json())

            self.agent.set_tools(result.tools)


    async def arun(self):
        session = PromptSession()

        while True:
            try:
                text = await session.prompt_async("> ")
                self._handle_input_text(text)
            except (KeyboardInterrupt, EOFError):
                break

    def _handle_input_text(self, text: str):
        if len(text) > 0:
            self.agent.invoke(text)
