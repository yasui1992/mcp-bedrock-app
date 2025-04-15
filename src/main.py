import asyncio
from mcpapp import REPL, MCPClient


async def main():
    client = MCPClient()
    async with client.aconnent_session() as session:
        repl = REPL()
        await repl.arun()

        session  # NOTE: Temporary usage to avoid F841


if __name__ == "__main__":
    asyncio.run(main())
