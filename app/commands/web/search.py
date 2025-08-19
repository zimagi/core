from systems.commands.index import Command


class Search(Command("web.search")):

    def exec(self):
        results = self.search_web(self.search_text, self.search_provider, self.max_results)
        if results:
            self.success(f"Found {len(results)} web search results:")
            for result in results:
                self.data(result.url, result.export(), "web_search_results")
        else:
            self.notice("No webpages found matching search criteria")
