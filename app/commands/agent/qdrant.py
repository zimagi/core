from systems.commands.index import Agent


class Qdrant(Agent("qdrant")):
    processes = ("qdrant_backup", "qdrant_clean", "qdrant_restore")

    def qdrant_backup(self):
        for package in self.listen("db:backup:init", state_key="qdrant"):
            self.create_snapshot()

    def qdrant_clean(self):
        for package in self.listen("db:clean", state_key="qdrant"):
            self.clean_snapshots(keep_num=package.message)

    def qdrant_restore(self):
        for package in self.listen("db:restore:init", state_key="qdrant"):
            if package.message.get("latest", False):
                self.restore_snapshot()
