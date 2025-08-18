import os

from django.conf import settings
from systems.plugins.index import BaseProvider
from utility.data import ensure_list


class Provider(BaseProvider("encoder", "transformer")):

    def initialize_model(self):
        os.environ["HF_HOME"] = settings.MANAGER.hf_cache

    @property
    def transformer(self):
        if not getattr(self, "_transformer", None):
            from sentence_transformers import SentenceTransformer

            self._transformer = SentenceTransformer(
                self.field_model,
                cache_folder=settings.MANAGER.st_model_cache,
                device=self.field_device,
                token=settings.HUGGINGFACE_TOKEN,
            )
        return self._transformer

    def encode(self, text):
        if not text:
            return []
        return self.transformer.encode(ensure_list(text)).tolist()
