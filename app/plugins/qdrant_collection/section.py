from systems.plugins.index import BaseProvider


class Provider(BaseProvider("qdrant_collection", "section")):

    def _get_index_fields(self):
        return {
            "library": "keyword",
            "path": "keyword",
            "order": "float",
        }

    def _get_section_filters(self, library=None, path=None):
        from qdrant_client import models

        filters = []

        if library:
            filters.append(self._get_query_id_condition("library", library))
        if path:
            filters.append(self._get_query_id_condition("path", path))

        return models.Filter(must=filters) if filters else None

    def count(self, library=None, path=None):
        return self._get_count_query(self._get_section_filters(library, path))

    def exists(self, library=None, path=None):
        return self._check_exists(self._get_section_filters(library, path))

    def get(
        self,
        library=None,
        path=None,
        fields=None,
        include_vectors=False,
    ):
        return self._run_query(
            self._get_section_filters(library, path),
            fields=fields,
            include_vectors=include_vectors,
        )

    def store(self, library, path, text, embedding, order):
        return self.request_upsert(
            collection_name=self.get_collection_name(),
            points=[
                self._get_record(
                    text,
                    embedding,
                    library=library,
                    path=path,
                    order=order,
                )
            ],
        )

    def remove(self, library=None, path=None):
        return self.request_delete(
            collection_name=self.get_collection_name(),
            points_selector=self._get_section_filters(library, path),
        )
