from systems.commands.index import Command


class Search(Command("web.search")):

    def exec(self):
        # Search the web
        results = self.search_web(self.search_text, self.max_results)
        if results:
            self.success(f"Found {len(results)} web search results:")
            for result in results:
                self.data(result["url"], result, "result")
        else:
            self.notice("No webpages found matching search criteria")
