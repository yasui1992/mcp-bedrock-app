import asyncio
import logging
import os
import traceback

import boto3
from botocore.config import Config
from mcpapp import BedrockAgent, MCPClient, REPL


LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()


class OneLineFormatter(logging.Formatter):
    def formatException(self, exc_info):
        return ''.join(traceback.format_exception(*exc_info)).replace("\n", "\\n")

# ロガーの設定
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = OneLineFormatter(r"%(asctime)s %(levelname)-8s %(message)s %(exception)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


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
