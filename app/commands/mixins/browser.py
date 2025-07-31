import re

from bs4 import BeautifulSoup
from systems.commands.index import CommandMixin
from utility.data import Collection
from utility.web import WebParser


class BrowserMixin(CommandMixin("browser")):

    def parse_webpage(self, url):
        webpage = self.submit("browser:request", url, timeout=30)
        browser = None
        text = ""

        if webpage["source"]:
            source = webpage["source"]
            soup, text = self._parse_webpage_text(webpage["source"])
        if not text:
            browser = WebParser(url, verify=False)
            source = browser.text
            soup, text = self._parse_webpage_text(browser.text)

        return Collection(
            url=webpage["url"] if not browser else url,
            title=soup.title.text.encode("ascii", errors="ignore").decode().strip() if soup.title else "",
            source=source,
            text=text,
            soup=soup,
        )

    def _parse_webpage_text(self, text):
        soup = BeautifulSoup(text, "html.parser")
        text = re.sub(r"\n+", "\n", soup.get_text("\n")).encode("ascii", errors="ignore").decode().strip()
        return soup, text
