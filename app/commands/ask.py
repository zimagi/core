from systems.commands.index import Command


class Ask(Command("ask")):

    def exec(self):
        response = self.generate_text(self.instruction_text, **self.model_options)

        self.data("Answer", response["text"], "answer")
        self.spacing()
        self.data("Reasoning", response["reasoning"], "reasoning")
