from systems.commands.index import Command


class Snapshot(Command("qdrant.snapshot")):

    def exec(self):
        self.create_snapshot(self.collection_name)
