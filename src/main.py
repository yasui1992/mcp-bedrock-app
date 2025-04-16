import asyncio
from mcpapp import REPL, MCPClient


async def main():
    client = MCPClient()
    repl = REPL(client)
    await repl.arun()


if __name__ == "__main__":
    asyncio.run(main())
