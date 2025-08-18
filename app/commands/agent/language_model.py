from systems.commands.index import Agent
from utility.data import Collection


class LanguageModelError(Exception):
    pass


class LanguageModel(Agent("language_model")):

    def exec(self):
        for package in self.listen("language_model:generate", state_key="language_model"):
            request = Collection(**package.message)
            try:
                with self.run_as(package.user) as user:
                    self.notice(f"Starting language model generation request: {request}")
                    response = self._process_generate_request(user, request)
                    metrics = Collection(
                        prompt_tokens=response.prompt_tokens,
                        output_tokens=response.output_tokens,
                        total_tokens=response.total_tokens,
                        cost=response.cost,
                    )
                    self.send(package.sender, response.export())
                    self.send("language_model:complete", metrics)

                    if self.manager.runtime.debug():
                        self.success(f"Response:\n\n{response.text}")
                        self.notice(f"Reasoning:\n\n{response.reasoning}")
                        self.data("Response metrics", metrics)

            except Exception as error:
                self.warning(f"Language model generate request failed with error: {error}:\n\n{request}")

    def _process_generate_request(self, user, request):
        try:
            language_model = user.get_language_model(self)
        except Exception as error:
            raise LanguageModelError(f"Language model encountered an error loading provider: {error}")

        return language_model.exec(request.messages, **(request.options or {}))
