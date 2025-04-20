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
fmt = logging.Formatter(r"%(asctime)s %(levelname)-8s %(name)s %(message)s")
hdlr.setFormatter(fmt)
logger.addHandler(hdlr)


async def main():
    client = MCPClient()

    async with client.aconnent_session() as session:
        agent = BedrockAgent(session)
        await agent.afetch_tools()

        repl = REPL(agent)

        await repl.arun()


if __name__ == "__main__":
    asyncio.run(main())
