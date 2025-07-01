from systems.plugins.index import BasePlugin
from utility.data import dump_json

import copy
import math


class LanguageModelResult(object):

    def __init__(self, text, reasoning="", prompt_tokens=0, output_tokens=0, cost=None):
        self.text = text
        self.reasoning = reasoning
        self.prompt_tokens = prompt_tokens
        self.output_tokens = output_tokens
        self.total_tokens = prompt_tokens + output_tokens
        self.cost = cost

    def __str__(self):
        return dump_json(self.__dict__, indent=2)

    def __repr__(self):
        return self.__str__()

    def export(self):
        return copy.deepcopy(self.__dict__)


class BaseProvider(BasePlugin("language_model")):

    def __init__(self, type, name, command, **options):
        super().__init__(type, name, command)
        self.import_config(options)
        self.initialize_model()

    def initialize_model(self):
        # Implement in subclasses if needed
        pass

    def get_context_length(self):
        raise NotImplementedError("Language Model providers must implement get_context_length method")

    def get_max_new_tokens(self):
        return math.floor(self.get_context_length() * self.field_max_token_percent)

    def get_max_tokens(self):
        return self.get_context_length() - self.get_max_new_tokens()

    def get_token_count(self, messages):
        raise NotImplementedError("Language Model providers must implement get_token_count method")

    def exec(self, messages):
        raise NotImplementedError("Language Model providers must implement exec method")
