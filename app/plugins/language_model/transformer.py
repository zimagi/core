from django.conf import settings

from systems.plugins.index import BaseProvider
from utility.data import dump_json
from .base import LanguageModelResult

import os


class Provider(BaseProvider("language_model", "transformer")):

    def initialize_model(self):
        os.environ["HF_HOME"] = settings.MANAGER.hf_cache

    @property
    def tokenizer(self):
        if not getattr(self, "_tokenizer", None):
            from transformers import AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(self.field_model, token=settings.HUGGINGFACE_TOKEN)
        return self._tokenizer

    @property
    def pipeline(self):
        if not getattr(self, "_pipeline", None):
            from transformers import pipeline

            self._pipeline = pipeline(
                "text-generation",
                model=self.field_model,
                device=self.field_device,
                use_auth_token=settings.HUGGINGFACE_TOKEN,
            )
        return self._pipeline

    def get_context_length(self):
        return self.tokenizer.model_max_length

    def get_token_count(self, messages):
        if isinstance(messages, str):
            return len(self.tokenizer(messages)["input_ids"])
        return len(self.tokenizer(dump_json(messages))["input_ids"])

    def exec(self, messages):
        results = self.pipeline(
            messages,
            do_sample=True,
            temperature=self.field_temperature,
            top_k=self.field_top_k,
            top_p=self.field_top_p,
            num_return_sequences=1,
            return_full_text=False,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=self.get_max_new_tokens(),
        )
        return LanguageModelResult(
            results[0]["generated_text"],
            prompt_tokens=self.get_token_count(messages),
            output_tokens=self.get_token_count(results[0]["generated_text"]),
        )
