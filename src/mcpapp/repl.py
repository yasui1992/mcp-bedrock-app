from prompt_toolkit import PromptSession


# TODO: Create an interface protocol to support other IFs (e.g., REST API)
class REPL:
    async def arun(self):
        session = PromptSession()

        while True:
            try:
                text = await session.prompt_async("> ")
            except (KeyboardInterrupt, EOFError):
                break

        text  # NOTE: Temporary usage to avoid F841
