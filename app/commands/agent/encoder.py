from systems.commands.index import Agent
from utility.data import Collection


class EncodingError(Exception):
    pass


class Encoder(Agent("encoder")):

    def exec(self):
        primary_user = self.active_user

        for package in self.listen("encoder:save", state_key="encoder"):
            request = Collection(**package.message)
            if not request.payload:
                request.payload = {}
            try:
                with self.run_as(request.user) as user:
                    self._process_request(user, request)

                self.success(f"Successfully encoded: {request}")
                self.send("encoder:complete", package.message)

            except Exception as error:
                self.warning(f"Encoder request failed with error: {error}:\n\n{request}")

    def _process_request(self, user, request):
        try:
            text_splitter = user.get_text_splitter(self)
            encoder = user.get_encoder(self)

            instance = self.facade(request.data_type).retrieve_by_id(request.id)
            field_value = getattr(instance, request.field, None) if instance else None

        except Exception as error:
            raise EncodingError(f"Encoder encountered an error retrieving instance: {error}")

        if not field_value:
            raise EncodingError(f"Encoding request is missing input value for field {request.field}")

        sections = text_splitter.split(field_value)
        embeddings = encoder.encode(sections)
        collection = user.get_qdrant_collection(self, request.collection)
        schema = collection.get_info().schema

        for index, text in enumerate(sections):
            collection.store(
                **self._get_payload_fields(request, schema, index),
                text=text,
                embedding=embeddings[index],
            )

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
