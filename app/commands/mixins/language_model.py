from plugins.language_model.base import LanguageModelResult
from systems.commands.index import CommandMixin
from utility.data import ensure_list


class LanguageModelMixin(CommandMixin("language_model")):

    def generate_text(self, messages, **options):
        return LanguageModelResult(
            **self.submit(
                "language_model:generate",
                {
                    "messages": ensure_list(messages),
                    "options": options,
                },
            )
        )
