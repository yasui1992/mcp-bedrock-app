
from contextlib import asynccontextmanager
import logging
import os
from typing import AsyncGenerator, Final

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


FASTMCP_LOG_LEVEL: Final[str] = os.getenv("FASTMCP_LOG_LEVEL", "error").upper()


logger = logging.getLogger("mcpapp.client")


class MCPClient:
    def __init__(self):
        # TODO: Allow external injection of the MCP server instance
        self._server_params = StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-documentation-mcp-server@latest"],
            env={
                "FASTMCP_LOG_LEVEL": FASTMCP_LOG_LEVEL
            }
        )

    @asynccontextmanager
    async def aconnent_session(self) -> AsyncGenerator[ClientSession, None]:
        async with stdio_client(self._server_params) as rw:
            async with ClientSession(*rw) as session:
                init_result = await session.initialize()
                logger.debug(init_result.model_dump_json())

                yield session
