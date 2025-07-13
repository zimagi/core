from systems.commands.index import Command


class Restore(Command("qdrant.restore")):

    def exec(self):
        self.restore_snapshot(self.collection_name, self.snapshot_name)
