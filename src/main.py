import asyncio
import logging
import os

import boto3
from botocore.config import Config
from mcpapp import BedrockAgent, MCPClient, REPL


LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()


logger = logging.getLogger("mcpapp")
logger.setLevel(LOG_LEVEL)
hdlr = logging.StreamHandler()
hdlr.setLevel(logging.NOTSET)
fmt = logging.Formatter(r"%(asctime)s %(levelname)-8s %(name)s %(message)s")
hdlr.setFormatter(fmt)
logger.addHandler(hdlr)


async def main():
    boto3_config = Config(
        retries={
            "max_attempts": 10,
            "mode": "adaptive"
        }
    )

    mcp_client = MCPClient()
    llm_client = boto3.client("bedrock-runtime", config=boto3_config)

    async with mcp_client.aconnent_session() as session:
        agent = BedrockAgent(session, llm_client)
        await agent.afetch_tools()

        repl = REPL(agent)

        await repl.arun()


if __name__ == "__main__":
    asyncio.run(main())
