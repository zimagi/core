from systems.commands.index import Command


class List(Command("qdrant.list")):

    def exec(self):
        for collection in self.get_qdrant_collections(self.collection_name):
            info = collection.get_info()

            self.info(self.display_width * "=")
            self.info(" Qdrant Collection: {}".format(self.key_color(collection.name)))

            status = info.status
            if status == "green":
                status = self.green(info.status)
            elif status == "yellow":
                status = self.yellow(info.status)
            elif status == "red":
                status = self.red(info.status)

            self.table(
                [
                    ["Status", status],
                    ["Optimizer", self.value_color(info.optimizer)],
                    ["Segment Count", self.value_color(info.segment_count)],
                    ["Point Count", self.value_color(info.point_count)],
                    ["Vector Count", self.value_color(info.vector_count)],
                    ["Indexed Vector Count", self.value_color(info.indexed_vector_count)],
                ]
            )
            self.info("")

            for snapshot in collection.list_snapshots():
                self.info(
                    " [ {} ] {} ({} mb)".format(
                        self.value_color(snapshot.creation_time),
                        self.key_color(snapshot.name),
                        self.value_color(int(snapshot.size / 1048576)),  # MB
                    )
                )

            self.info("")
