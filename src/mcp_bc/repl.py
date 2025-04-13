from prompt_toolkit import PromptSession



class REPL:
    def run(self):
        session = PromptSession()

        while True:
            try:
                text = session.prompt("> ")
            except (KeyboardInterrupt, EOFError):
                break
