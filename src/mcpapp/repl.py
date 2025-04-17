import json
import logging
import os
from typing import Final

import boto3
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
    # TODO: Resolve hard-coding
    BEDROCK_MODEL_ID: Final[str] = "anthropic.claude-3-haiku-20240307-v1:0"

    def __init__(self):
        self._llm_client = boto3.client("bedrock-runtime")

        self._tools = []

    async def aset_mcp_client(self, mcp_client: MCPClient):
        async with mcp_client.aconnent_session() as mcp_session:
            result = await mcp_session.list_tools()
            logger.debug(result.model_dump_json())

            self._tools = result.tools

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
            self._converse(text)

    def _converse(self, text: str):
            messages = [
                {"role": "user", "content": [ { "text": text } ]}
            ]

            # TODO: Resolve too deeply nested
            response = self._llm_client.converse(
                modelId=self.BEDROCK_MODEL_ID,
                messages=messages,
                toolConfig={
                    "tools": [
                        {
                            "toolSpec": {
                                "name": t.name,
                                "description": t.description,
                                "inputSchema": {
                                    "json": t.inputSchema
                                }
                            }
                        }
                        for t in self._tools
                    ]
                }
            )
            logger.debug(json.dumps(response))

            # NOTE: Response print is temporary
            print(response)
