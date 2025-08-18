from systems.commands.index import Command


class Browser(Command("browser")):

    def exec(self):
        self.data("HTML Webpage", self.submit("browser:request", self.url), "webpage_html")
