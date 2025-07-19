from systems.commands.index import CommandMixin
from utility.data import Collection, ensure_list


class QdrantMixin(CommandMixin("qdrant")):

    def qdrant(self, name, **options):
        return self.get_provider("qdrant_collection", name, **options)

    def get_qdrant_collections(self, names=None, **options):
        if names:
            return [self.qdrant(name, **options) for name in ensure_list(names)]
        return [
            self.qdrant(name, **options)
            for name in list(self.manager.index.get_plugin_providers("qdrant_collection").keys())
        ]

    def _get_qdrant_collection(self, collection, **options):
        if isinstance(collection, str):
            return self.qdrant(collection, **options)
        return collection

    def get_embeddings(self, collection, **filters):
        qdrant = self._get_qdrant_collection(collection)
        texts = []
        embeddings = []

        for result in qdrant.get(fields="text", include_vectors=True, **filters):
            texts.append(result.payload["text"])
            embeddings.append(result.vector)

        return Collection(texts=texts, embeddings=embeddings)

    def search_embeddings(
        self, collection, embeddings, fields=None, limit=10, min_score=0, filter_field=None, filter_ids=None
    ):
        if not embeddings:
            return []

        qdrant = self._get_qdrant_collection(collection)

        if fields is None:
            fields = []
        if filter_field:
            fields = [filter_field, *fields]

        options = {"limit": limit, "min_score": min_score, "fields": [*fields, "text"]}
        if filter_field and filter_ids:
            options["filter_field"] = filter_field
            options["filter_values"] = ensure_list(filter_ids)

        return qdrant.search(embeddings, **options)

    def create_snapshot(self, collection_name=None):
        def _create_snapshot(collection):
            collection.create_snapshot()
            self.success(f"Qdrant snapshot for {collection.name} successfully created")

        results = self.run_list(self.get_qdrant_collections(collection_name), _create_snapshot)
        if results.aborted:
            self.error("Qdrant snapshot creation failed")

    def remove_snapshot(self, collection_name, snapshot_name):
        collection = self.qdrant(collection_name)
        if not collection.delete_snapshot(snapshot_name):
            self.warning(f"Qdrant snapshot {snapshot_name} not removed")
        self.success(f"Qdrant snapshot {snapshot_name} successfully removed")

    def clean_snapshots(self, collection_name=None, keep_num=3):
        def _clean_snapshots(collection):
            collection.clean_snapshots(keep_num)
            self.success(f"Qdrant snapshots for {collection.name} successfully cleaned")

        results = self.run_list(self.get_qdrant_collections(collection_name), _clean_snapshots)
        if results.aborted:
            self.error("Qdrant snapshot cleaning failed")

    def restore_snapshot(self, collection_name=None, snapshot_name=None):
        def _restore_snapshot(collection):
            collection.restore_snapshot()
            self.success(f"Latest Qdrant snapshot for {collection.name} successfully restored")

        if snapshot_name:
            if not collection_name:
                self.error("Collection name required when specifying the snapshot name to restore")

            collection = self.qdrant(collection_name)
            if not collection.restore_snapshot(snapshot_name):
                self.error(f"Qdrant snapshot {snapshot_name} restore failed")
            self.success(f"Qdrant snapshot {snapshot_name} successfully restored")
        else:
            results = self.run_list(self.get_qdrant_collections(collection_name), _restore_snapshot)
            if results.aborted:
                self.error("Qdrant snapshot restoration failed")
