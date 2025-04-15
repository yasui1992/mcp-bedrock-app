from prompt_toolkit import PromptSession



class REPL:
    async def arun(self):
        session = PromptSession()

        while True:
            try:
                text = await session.prompt_async("> ")
            except (KeyboardInterrupt, EOFError):
                break

        text  # NOTE: Temporary usage to avoid F841
