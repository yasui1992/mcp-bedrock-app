import asyncio
import logging
import os
from typing import Final

from mcpapp import BedrockAgent, MCPClient, REPL


LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "info").upper()


logger = logging.getLogger("mcpapp")
logger.setLevel(LOG_LEVEL)
hdlr = logging.StreamHandler()
hdlr.setLevel(logging.NOTSET)
hdlr.setFormatter(logging.Formatter(r"%(asctime)s %(levelname)-8s %(message)s"))
logger.addHandler(hdlr)


async def main():
    client = MCPClient()
    agent = BedrockAgent()
    repl = REPL(agent)

    await repl.aset_mcp_client(client)
    await repl.arun()


if __name__ == "__main__":
    asyncio.run(main())
