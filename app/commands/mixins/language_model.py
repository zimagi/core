from plugins.language_model.base import LanguageModelResult
from systems.commands.index import CommandMixin
from utility.data import ensure_list


class LanguageModelMixin(CommandMixin("language_model")):

    def instruct(self, user, messages, **options):
        with self.run_as(user) as user:
            return LanguageModelResult(
                **self.submit(
                    "language_model:generate",
                    {
                        "messages": ensure_list(messages),
                        "options": options,
                    },
                )
            )
