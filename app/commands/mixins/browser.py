from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown
from systems.commands.index import CommandMixin
from utility.data import Collection
from utility.web import WebParser


class BrowserMixin(CommandMixin("browser")):

    def parse_webpage(self, url):
        webpage = self.submit("browser:request", url, timeout=30)
        browser = None
        source = ""

        if webpage["source"]:
            source = webpage["source"]
        if not source:
            browser = WebParser(url, verify=False)
            source = browser.text

        soup = BeautifulSoup(source, "lxml")
        return Collection(
            url=webpage["url"] if not browser else url,
            title=soup.title.text.encode("ascii", errors="ignore").decode().strip() if soup.title else "",
            source=source,
            text=convert_to_markdown(soup),
            soup=soup,
        )
