import re
import statistics

import requests
from bs4 import BeautifulSoup

from .data import ensure_list


class WebParserError(Exception):
    pass


class WebParser:

    def __init__(self, urls, verify=True, timeout=5):
        self.urls = ensure_list(urls)
        self.texts = []
        self.url = None

        self.soup = None
        self.verify = verify
        self.timeout = timeout
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"}

        self._download()

    @property
    def text(self):
        return "\n\n".join(self.texts)

    def _download(self):
        for url in self.urls:
            try:
                response = requests.get(url, headers=self.headers, verify=self.verify, timeout=self.timeout)
                self.url = response.url

            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                raise WebParserError(f"Web Request {url} failed with: {e}")

            if response.status_code == 200:
                self.soup = BeautifulSoup(response.content, features="html.parser")

                text = re.sub(r"\n+", "\n", self.soup.get_text("\n")).encode("ascii", errors="ignore").decode().strip()
                lines = [line.strip() for line in text.split("\n") if line.strip()]

                if len(lines) > 1:
                    quartiles = statistics.quantiles([len(line) for line in lines], n=3)
                    lines = ["{}.".format(line.rstrip(".")) for line in lines if len(line) > quartiles[0]]

                self.texts.append("  ".join(lines))
            else:
                raise WebParserError(f"Web Request failed with {response.status_code}: {url}")
