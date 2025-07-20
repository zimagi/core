from django.conf import settings
from systems.commands.index import CommandMixin
from utility.data import Collection, ensure_list


class QdrantMixin(CommandMixin("qdrant")):

    def save_embeddings(self, data_type, id, field, collection=None, payload=None):
        if collection is None:
            collection = data_type
        if payload is None:
            payload = {}

        self.send(
            "encoder:save",
            {
                "data_type": data_type,
                "id": id,
                "field": field,
                "collection": collection,
                "payload": payload,
            },
        )

    def get_search_embeddings(self, text):
        return self.submit("encoder:search", text)

    @property
    def qdrant_client(self):
        if not getattr(self, "_qdrant_client", None):
            from qdrant_client import QdrantClient

            self._qdrant_client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                https=settings.QDRANT_HTTPS,
                api_key=settings.QDRANT_ACCESS_KEY,
                timeout=14400,
            )
        return self._qdrant_client

    def get_qdrant_collections(self, names=None):
        names = ensure_list(names) if names else []
        collections = []

        def check_name(collection_name, check_names):
            for name in check_names:
                if collection_name.startswith(name):
                    return True
            return False

        for collection in self.qdrant_client.get_collections():
            if not names or check_name(collection.name, names):
                name_components = collection.name.split("--")
                if len(name_components) > 1:
                    collections.append(
                        self.get_provider("qdrant_collection", name_components[0], dimension=name_components[1])
                    )
                else:
                    collections.append(self.get_provider("qdrant_collection", name_components[0]))

        return collections

    def get_embeddings(self, collection, **filters):
        texts = []
        embeddings = []

        for result in collection.get(fields="text", include_vectors=True, **filters):
            texts.append(result.payload["text"])
            embeddings.append(result.vector)

        return Collection(texts=texts, embeddings=embeddings)

    def search_embeddings(self, collection, text, fields=None, limit=10, min_score=0, filter_field=None, filter_ids=None):
        embeddings = self.get_search_embeddings(text) if text else []
        if not embeddings:
            return []

        if fields is None:
            fields = []
        if filter_field:
            fields = [filter_field, *fields]

        options = {"limit": limit, "min_score": min_score, "fields": [*fields, "text"]}
        if filter_field and filter_ids:
            options["filter_field"] = filter_field
            options["filter_values"] = ensure_list(filter_ids)

        return collection.search(embeddings, **options)

    def create_snapshot(self, collection_names=None):
        def _create_snapshot(collection):
            collection.create_snapshot()
            self.success(f"Qdrant snapshot for {collection.name} successfully created")

        results = self.run_list(self.get_qdrant_collections(collection_names), _create_snapshot)
        if results.aborted:
            self.error("Qdrant snapshot creation failed")

    def remove_snapshot(self, collection_names, snapshot_name):
        def _remove_snapshot(collection):
            if not collection.delete_snapshot(snapshot_name):
                self.warning(f"Qdrant snapshot {snapshot_name} for {collection.name} not removed")
            self.success(f"Qdrant snapshot {snapshot_name} for {collection.name} successfully removed")

        results = self.run_list(self.get_qdrant_collections(collection_names), _remove_snapshot)
        if results.aborted:
            self.error("Qdrant snapshot removal failed")

    def clean_snapshots(self, collection_names=None, keep_num=3):
        def _clean_snapshots(collection):
            collection.clean_snapshots(keep_num)
            self.success(f"Qdrant snapshots for {collection.name} successfully cleaned")

        results = self.run_list(self.get_qdrant_collections(collection_names), _clean_snapshots)
        if results.aborted:
            self.error("Qdrant snapshot cleaning failed")

    def restore_snapshot(self, collection_names=None, snapshot_name=None):
        def _restore_snapshot(collection):
            if snapshot_name:
                if not collection.restore_snapshot(snapshot_name):
                    self.error(f"Qdrant snapshot {snapshot_name} for {collection.name} restore failed")
                self.success(f"Qdrant snapshot {snapshot_name} for {collection.name} successfully restored")
            else:
                if not collection.restore_snapshot():
                    self.error(f"Latest Qdrant snapshot for {collection.name} restore failed")
                self.success(f"Latest Qdrant snapshot for {collection.name} successfully restored")

        results = self.run_list(self.get_qdrant_collections(collection_names), _restore_snapshot)
        if results.aborted:
            self.error("Qdrant snapshot restoration failed")
