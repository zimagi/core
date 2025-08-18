from systems.commands.index import Command


class Search(Command("file.search")):

    def exec(self):
        results = self.search_files(self.library_name, self.search_text, self.max_results)
        if results:
            self.success(f"Found {len(results)} files:")
            for result in results:
                self.data(result["path"], result, "result")
        else:
            self.notice("No files found matching search criteria")
