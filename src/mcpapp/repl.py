import logging
import os
from typing import Final

from prompt_toolkit import PromptSession

from mcpapp.client import MCPClient


LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "info").upper()

logger = logging.getLogger("mcpapp.client")
logger.setLevel(LOG_LEVEL)
hdlr = logging.StreamHandler()
hdlr.setLevel(logging.NOTSET)
hdlr.setFormatter(logging.Formatter(r"%(asctime)s %(levelname)-8s %(message)s"))
logger.addHandler(hdlr)


# TODO: Create an interface protocol to support other IFs (e.g., REST API)
class REPL:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client

    async def arun(self):
        session = PromptSession()

        async with self.mcp_client.aconnent_session() as mcp_session:
            tools = await mcp_session.list_tools()
            logger.debug(tools.model_dump_json())

            while True:
                try:
                    text = await session.prompt_async("> ")
                except (KeyboardInterrupt, EOFError):
                    break

            text  # NOTE: Temporary usage to avoid F841
