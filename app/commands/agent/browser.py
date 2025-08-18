from systems.commands.index import Agent
from utility.browser import Browser as WebBrowser
from utility.data import Collection


class Browser(Agent("browser")):

    def exec(self):
        channel = "browser:request"

        for package in self.listen(channel, state_key="browser"):
            url = package.message

            try:
                self.data("Processing browser request", package.sender)
                response = self.profile(self._fetch_html, url)
                self.send(package.sender, response.result.export())

            except Exception as error:
                self.send(channel, package.message, package.sender)
                raise error

            self.send(
                f"{channel}:stats",
                {
                    "url": url,
                    "final_url": response.result.url,
                    "html_length": len(response.result.source),
                    "time": response.time,
                    "memory": response.memory,
                },
            )

    def _fetch_html(self, url):
        browser = WebBrowser(url)
        return Collection(source=browser.source, url=browser.final_url)
