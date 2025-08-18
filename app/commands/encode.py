from systems.commands.index import Command


class Encode(Command("encode")):

    def exec(self):
        embeddings = self.get_search_embeddings(self.active_user, self.source_text)

        if self.display_embeddings:
            self.data("Embeddings", embeddings, "embeddings")
        else:
            self.silent_data("embeddings", embeddings)

        self.success("Successfully generated embeddings from source text")
