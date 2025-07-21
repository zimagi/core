import re

from systems.commands.index import Agent
from utility.data import Collection


class EncodingError(Exception):
    pass


class EncodingProviders:
    def __init__(self, text_splitter, encoder):
        self.text = text_splitter
        self.encoder = encoder


class Encoder(Agent("encoder")):
    processes = ("encoder_save", "encoder_search", "encoder_remove")

    prefix_ignore_pattern = r"^(\@[a-zA-Z0-9]+(\s*\,)?\s*)+\s*\:\s*"

    def encoder_save(self):
        for package in self.listen("encoder:save", state_key="encoder"):
            request = Collection(**package.message)
            try:
                with self.run_as(package.user) as user:
                    self._process_save_request(user, request)
                    self.success(f"Successfully encoded: {request}")
                    self.send("encoder:complete", package.message)

            except Exception as error:
                self.warning(f"Encoder save request failed with error: {error}:\n\n{request}")

    def encoder_search(self):
        for package in self.listen("encoder:search", state_key="encoder"):
            try:
                with self.run_as(package.user) as user:
                    embeddings = self._process_search_request(user, package.message)
                    self.success(f"Successfully encoded: {package.message}")
                    self.send(package.sender, embeddings)

            except Exception as error:
                self.warning(f"Encoder search request failed with error: {error}:\n\n{package.message}")

    def encoder_remove(self):
        for package in self.listen("encoder:remove", state_key="encoder"):
            request = Collection(**package.message)
            try:
                with self.run_as(package.user) as user:
                    self._process_delete_request(user, request)
                    self.success(f"Successfully removed embeddings: {request}")

            except Exception as error:
                self.warning(f"Encoder remove request failed with error: {error}:\n\n{request}")

    def _process_save_request(self, user, request):
        try:
            instance = self.facade(request.data_type).retrieve_by_id(request.id)
            field_value = getattr(instance, request.field, None) if instance else None

        except Exception as error:
            raise EncodingError(f"Encoder encountered an error retrieving instance: {error}")
        if not field_value:
            raise EncodingError(f"Encoding request is missing input value for field {request.field}")

        provider = self._get_encoding_providers(user)
        sections = provider.text.split(re.sub(self.prefix_ignore_pattern, "", field_value).capitalize())
        embeddings = provider.encoder.encode(sections)
        collection = user.get_qdrant_collection(self, request.collection)
        schema = collection.get_info().schema

        for index, text in enumerate(sections):
            collection.store(
                **self._get_payload_fields(request, schema, index),
                text=text,
                embedding=embeddings[index],
            )

    def _process_search_request(self, user, text):
        if not text:
            raise EncodingError("Encoding request is missing input text")

        provider = self._get_encoding_providers(user)
        return provider.encoder.encode(provider.text.split(re.sub(self.prefix_ignore_pattern, "", text).capitalize()))

    def _process_delete_request(self, user, request):
        collection = user.get_qdrant_collection(self, request.collection)
        collection.remove(self._get_filter_fields(request, collection.get_info().schema))

    def _get_encoding_providers(self, user):
        try:
            text_splitter = user.get_text_splitter(self)
            encoder = user.get_encoder(self)

        except Exception as error:
            raise EncodingError(f"Encoder encountered an error getting encoding providers: {error}")

        return EncodingProviders(text_splitter, encoder)

    def _get_payload_fields(self, request, schema, index):
        payload = {}
        for field_name in ["order", *list(request.payload.keys())]:
            if field_name in schema:
                if field_name == "order":
                    payload[field_name] = index
                else:
                    payload[field_name] = request.payload[field_name]
            else:
                self.warning(f"Field name {field_name} is not in schema for Qdrant collection: {request}")
        return payload

    def _get_filter_fields(self, request, schema):
        filters = {}
        for field_name in request.filters.keys():
            if field_name in schema:
                filters[field_name] = request.filters[field_name]
            else:
                self.warning(f"Field name {field_name} is not in schema for Qdrant collection: {request}")
        return filters
