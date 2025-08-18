from django.conf import settings
from googleapiclient.discovery import build
from systems.plugins.index import BaseProvider

from .base import SearchResult


class Provider(BaseProvider("search_engine", "google")):

    def search(self, query, max_results=10):
        try:
            if not settings.GOOGLE_SEARCH_API_KEY or not settings.GOOGLE_SEARCH_ID:
                self.command.error(
                    "To use the Google Custom Search Service you must specify "
                    "ZIMAGI_GOOGLE_SEARCH_API_KEY and ZIMAGI_GOOGLE_SEARCH_ID environment variables"
                )

            service = build("customsearch", "v1", developerKey=settings.GOOGLE_SEARCH_API_KEY)
            search = (
                service.cse()
                .list(q=query, cx=settings.GOOGLE_SEARCH_ID, num=min(max_results, 10))  # Google API max is 10 per request
                .execute()
            )
            results = []
            if "items" in search:
                for item in search["items"]:
                    result = SearchResult(item.get("link", None), item.get("title", ""), item.get("snippet", ""))
                    if result.url:
                        results.append(result)
            return results

        except Exception as error:
            self.command.error(f"Google Custom Search failed: {str(error)}")
