from systems.plugins.index import BaseProvider


class Provider(BaseProvider("qdrant_collection", "library")):

    def _get_index_fields(self):
        return {
            "library": "keyword",
            "path": "keyword",
            "section_id": "keyword",
            "order": "float",
        }

    def _get_library_filters(self, library=None, path=None, section_id=None):
        from qdrant_client import models

        filters = []

        if library:
            filters.append(self._get_query_id_condition("library", library))
        if path:
            filters.append(self._get_query_id_condition("path", path))
        if section_id:
            filters.append(self._get_query_id_condition("section_id", section_id))

        return models.Filter(must=filters) if filters else None

    def count(self, library=None, path=None, section_id=None):
        return self._get_count_query(self._get_library_filters(library, path, section_id))

    def exists(self, library=None, path=None, section_id=None):
        return self._check_exists(self._get_library_filters(library, path, section_id))

    def get(
        self,
        library=None,
        path=None,
        section_id=None,
        fields=None,
        include_vectors=False,
    ):
        return self._run_query(
            self._get_library_filters(library, path, section_id),
            fields=fields,
            include_vectors=include_vectors,
        )

    def store(self, library, path, section_id, text, embedding, order):
        return self.request_upsert(
            collection_name=self.get_collection_name(),
            points=[
                self._get_record(
                    text,
                    embedding,
                    library=library,
                    path=path,
                    section_id=section_id,
                    order=order,
                )
            ],
        )

    def remove(self, library=None, path=None, section_id=None):
        return self.request_delete(
            collection_name=self.get_collection_name(),
            points_selector=self._get_library_filters(library, path, section_id),
        )
