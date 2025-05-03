
from contextlib import asynccontextmanager
import json
import logging
import os
from typing import AsyncGenerator

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


APP_DIR = "/app"
CONFIG_FILENAME = "mcp_servers.json"


logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self):
        self._server_params = self._load_config()

    @asynccontextmanager
    async def aconnent_session(self) -> AsyncGenerator[ClientSession, None]:
        async with stdio_client(self._server_params) as rw:
            async with ClientSession(*rw) as session:
                init_result = await session.initialize()
                logger.debug(init_result.model_dump_json())

                yield session

    def _load_config(self) -> StdioServerParameters:
        config_filepath = os.path.join(APP_DIR, CONFIG_FILENAME)

        with open(config_filepath) as f:
            config = json.load(f)
        logger.debug(json.dumps(config))

        mcp_servers = config["mcpServers"]
        if len(mcp_servers) > 1:
            raise ValueError("Unsupported multi-mcp servers")

        server_params = next(iter(mcp_servers.values()))
        return StdioServerParameters(**server_params)
