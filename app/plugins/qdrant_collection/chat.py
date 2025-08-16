from systems.plugins.index import BaseProvider


class Provider(BaseProvider("qdrant_collection", "memory")):

    def _get_index_fields(self):
        return {
            "memory_id": "keyword",
            "user_id": "keyword",
            "dialog_id": "keyword",
            "message_id": "keyword",
            "role": "keyword",
            "order": "float",
        }

    def _get_memory_filters(self, memory_id=None, user_id=None, dialog_id=None, message_id=None):
        from qdrant_client import models

        filters = []

        if memory_id:
            filters.append(self._get_query_id_condition("memory_id", memory_id))
        if user_id:
            filters.append(self._get_query_id_condition("user_id", user_id))
        if dialog_id:
            filters.append(self._get_query_id_condition("dialog_id", dialog_id))
        if message_id:
            filters.append(self._get_query_id_condition("message_id", message_id))

        return models.Filter(must=filters) if filters else None

    def count(self, memory_id=None, user_id=None, dialog_id=None, message_id=None):
        return self._get_count_query(self._get_memory_filters(memory_id, user_id, dialog_id, message_id))

    def exists(self, memory_id=None, user_id=None, dialog_id=None, message_id=None):
        return self._check_exists(self._get_memory_filters(memory_id, user_id, dialog_id, message_id))

    def get(
        self,
        memory_id=None,
        user_id=None,
        dialog_id=None,
        message_id=None,
        fields=None,
        include_vectors=False,
    ):
        return self._run_query(
            self._get_memory_filters(memory_id, user_id, dialog_id, message_id),
            fields=fields,
            include_vectors=include_vectors,
        )

    def store(self, memory_id, user_id, dialog_id, message_id, text, embedding, role, order):
        return self.request_upsert(
            collection_name=self.get_collection_name(),
            points=[
                self._get_record(
                    text,
                    embedding,
                    memory_id=memory_id,
                    user_id=user_id,
                    dialog_id=dialog_id,
                    message_id=message_id,
                    role=role,
                    order=order,
                )
            ],
        )

    def remove(self, memory_id=None, user_id=None, dialog_id=None, message_id=None):
        return self.request_delete(
            collection_name=self.get_collection_name(),
            points_selector=self._get_memory_filters(memory_id, user_id, dialog_id, message_id),
        )
