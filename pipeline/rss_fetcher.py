

# rss_fetcher.py


import feedparser
import logging
from feedparser import FeedParserDict
from filters import filter
from typing import List, Dict, cast, Optional
from haashi_pkg.utility import Logger


class RSSFeedFetcher:

    def __init__(self, logger: Optional[Logger] = None) -> None:

        self.URL = "https://nairametrics.com/feed/"
        self.filter = filter

        self.feed_list: List[Dict[str, str]] = []
        self.logger = logger or Logger(level=logging.INFO)

    def fetch_feed(self) -> List[Dict[str, str]]:

        feed = feedparser.parse(self.URL)
        entries = cast(List[FeedParserDict], feed.entries)

        self.logger.info(f"Fetched {len(entries)} entries from {self.URL}")

        if not entries:
            raise Exception("No entries found!")

        for entry in entries:

            title = cast(str, entry.get("title", "")).lower()
            # summary = cast(str, entry.get("summary", "")).lower()
            link = cast(str, entry.get("link", ""))
            timestamp = cast(str, entry.get("published", ""))

            # simple filter
            if any(k in title for k in self.filter):
                self.feed_list.append({
                    "title": title,
                    "link": link,
                    "timestamp": timestamp
                })

        return self.feed_list


if __name__ == "__main__":

    rss = RSSFeedFetcher()
    import json
    print(json.dumps(rss.fetch_feed(), indent=4))
