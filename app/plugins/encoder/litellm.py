from litellm import embedding
from systems.plugins.index import BaseProvider
from utility.data import ensure_list


class Provider(BaseProvider("encoder", "litellm")):

    def encode(self, text):
        if not text:
            return []
        response = embedding(model=self.field_model, input=ensure_list(text))
        return [data.embedding for data in response.data]
