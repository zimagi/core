import os
import re

import spacy
from systems.plugins.index import BaseProvider
from utility.filesystem import save_file


class Provider(BaseProvider("text_splitter", "spacy")):

    def initialize_model(self):
        model_state_file = f"/tmp/{self.field_model}.downloaded"
        if not os.path.exists(model_state_file):
            spacy.cli.download(self.field_model)
            save_file(model_state_file, self.command.time.now_string)

    @property
    def model(self):
        return spacy.load(self.field_model)

    def split(self, text):
        char_limit = 1000000

        def _get_sentences(inner_text):
            if len(inner_text) > char_limit:
                sentence_index = None
                for match in re.finditer(r"([^\.]\.|\?|\!)(?=\s+)", inner_text[:char_limit], re.MULTILINE):
                    sentence_index = match.end()
                sentence_index = sentence_index if sentence_index else char_limit

                sentences = [
                    *_get_sentences(inner_text[:sentence_index].strip()),
                    *_get_sentences(inner_text[sentence_index:].strip()),
                ]
            else:
                doc = self.model(inner_text)
                sentences = []

                for sentence in doc.sents:
                    if self.field_validate:
                        if sentence[0].is_title:
                            noun_count = 0
                            verb_count = 0

                            for token in sentence:
                                if token.pos_ in ["NOUN", "PROPN"]:
                                    noun_count += 1
                                elif token.pos_ == "VERB":
                                    verb_count += 1

                            if noun_count > 0 and verb_count > 0:
                                sentence = re.sub(r"\n+", " ", str(sentence)).strip()
                                if len(sentence) < self.field_max_sentence_length:
                                    sentences.append(str(sentence))
                    else:
                        sentences.append(str(sentence))
            return sentences

        return _get_sentences(text.strip())
