from systems.commands.index import Command


class Clean(Command("qdrant.clean")):

    def exec(self):
        self.clean_snapshots(self.collection_name, keep_num=self.keep_num)
