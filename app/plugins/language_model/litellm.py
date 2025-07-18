from litellm import completion, completion_cost, get_max_tokens, token_counter
from systems.plugins.index import BaseProvider

from .base import LanguageModelResult


class Provider(BaseProvider("language_model", "litellm")):

    def get_context_length(self):
        return get_max_tokens(self.field_model)

    def get_token_count(self, messages):
        if isinstance(messages, str):
            return token_counter(model=self.field_model, messages=[{"role": "user", "content": messages}])
        return token_counter(model=self.field_model, messages=messages)

    def exec(self, messages):
        response = completion(model=self.field_model, messages=messages, num_retries=3)
        return LanguageModelResult(
            response.choices[0].message.content,
            reasoning=response.choices[0].message.reasoning_content,
            prompt_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            cost=completion_cost(completion_response=response),
        )
