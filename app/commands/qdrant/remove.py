from systems.commands.index import Command


class Remove(Command("qdrant.remove")):

    def exec(self):
        self.remove_snapshot(self.collection_name, self.snapshot_name)
