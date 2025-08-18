import re
from urllib.parse import urlparse

from django.conf import settings


class WebCrawler:

    def __init__(self, command, max_depth=None):
        self.command = command

        self.pages = {}
        self.titles = {}
        self.statements = {}

        self.max_depth = max_depth

    def fetch(self, url):
        self._fetch(url)
        return self._process_pages()

    def _fetch(self, url, depth=0):
        def request_page(request_url):
            request_url = re.sub(r"\#.+$", "", request_url.strip(), flags=re.IGNORECASE)
            if request_url not in self.pages and self._check_domain(request_url) and self._check_format(request_url):
                self.command.data(f"Requesting URL ({depth})", request_url)
                webpage = self.command.parse_webpage(request_url)
                if webpage.text:
                    for statement in webpage.text.split("\n"):
                        statement = statement.strip()
                        if statement not in self.statements:
                            self.statements[statement] = [request_url]
                        else:
                            self.statements[statement].append(request_url)

                    self.titles[request_url] = webpage.title
                    self.pages[request_url] = webpage.text

                    if self.max_depth is None or depth < self.max_depth:
                        request_root = self._get_url_root(webpage.url)
                        for link in webpage.soup.find_all("a", href=True):
                            if link["href"]:
                                page_link = (
                                    "{}{}".format(request_root, link["href"]) if link["href"][0] == "/" else link["href"]
                                )
                                if re.match(rf"^{request_root}[^\.]", page_link):
                                    self._fetch(page_link, (depth + 1))

                    return True
            return False

        if re.match(r"^https?\:\/\/", url):
            request_page(url)

        elif url and "." in url:
            url = re.sub(r"^https?\:\/\/", "", url, flags=re.IGNORECASE)
            for protocol in ["https", "http"]:
                if request_page(f"{protocol}://{url}"):
                    return

    def _process_pages(self):
        for url, text in self.pages.items():
            statements = []
            for statement in text.split("\n"):
                statement = statement.strip()
                if statement in self.statements and len(self.statements[statement]) == 1:
                    statements.append(statement)
            self.pages[url] = "\n".join(statements)
        return self.pages

    def _get_url_root(self, url):
        components = urlparse(url)
        return f"{components.scheme}://{components.netloc}"

    def _check_format(self, test_url):
        components = urlparse(test_url)
        if re.search(r"\.(pdf|docx?|xlsx?)$", components.path, flags=re.IGNORECASE):
            return False
        return True

    def _check_domain(self, test_url):
        test_url = test_url.lower()
        for filter_domain in settings.WEBCRAWLER_FILTERED_DOMAINS:
            if filter_domain in test_url:
                return False
        return True
