from systems.plugins.index import BaseProvider


class Provider(BaseProvider("qdrant_collection", "chat")):

    def _get_index_fields(self):
        return {
            "chat_id": "keyword",
            "user_id": "keyword",
            "dialog_id": "keyword",
            "message_id": "keyword",
            "role": "keyword",
            "order": "float",
        }

    def _get_chat_filters(self, chat_id=None, user_id=None, dialog_id=None, message_id=None):
        from qdrant_client import models

        filters = []

        if chat_id:
            filters.append(self._get_query_id_condition("chat_id", chat_id))
        if user_id:
            filters.append(self._get_query_id_condition("user_id", user_id))
        if dialog_id:
            filters.append(self._get_query_id_condition("dialog_id", dialog_id))
        if message_id:
            filters.append(self._get_query_id_condition("message_id", message_id))

        return models.Filter(must=filters) if filters else None

    def count(self, chat_id=None, user_id=None, dialog_id=None, message_id=None):
        return self._get_count_query(self._get_chat_filters(chat_id, user_id, dialog_id, message_id))

    def exists(self, chat_id=None, user_id=None, dialog_id=None, message_id=None):
        return self._check_exists(self._get_chat_filters(chat_id, user_id, dialog_id, message_id))

    def get(
        self,
        chat_id=None,
        user_id=None,
        dialog_id=None,
        message_id=None,
        fields=None,
        include_vectors=False,
    ):
        return self._run_query(
            self._get_chat_filters(chat_id, user_id, dialog_id, message_id),
            fields=fields,
            include_vectors=include_vectors,
        )

    def store(self, chat_id, user_id, dialog_id, message_id, text, embedding, role, order):
        return self.request_upsert(
            collection_name=self.get_collection_name(),
            points=[
                self._get_record(
                    text,
                    embedding,
                    chat_id=chat_id,
                    user_id=user_id,
                    dialog_id=dialog_id,
                    message_id=message_id,
                    role=role,
                    order=order,
                )
            ],
        )

    def remove(self, chat_id=None, user_id=None, dialog_id=None, message_id=None):
        return self.request_delete(
            collection_name=self.get_collection_name(),
            points_selector=self._get_chat_filters(chat_id, user_id, dialog_id, message_id),
        )
