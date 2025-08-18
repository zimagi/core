import copy

from systems.plugins.index import BasePlugin
from utility.data import dump_json


class SearchResult:

    def __init__(self, url=None, title=None, snippet=None):
        self.url = url
        self.title = title
        self.snippet = snippet

    def __str__(self):
        return dump_json(self.__dict__, indent=2)

    def export(self):
        return copy.deepcopy(self.__dict__)


class BaseProvider(BasePlugin("search_engine")):

    def search(self, query, max_results=10):
        raise NotImplementedError("Method search must be implemented in search_engine providers")
