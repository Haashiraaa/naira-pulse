

# processor.py

import logging
from typing import List, Dict, Optional
from haashi_pkg.utility import Logger
from pipeline.scraper import NairametricsScraper
from pipeline.store import NewsStore
from pipeline.aliases import NewsLike


class NewsProcessor:

    def __init__(
        self,
        scraper: Optional[NairametricsScraper] = None,
        store: Optional[NewsStore] = None,
        logger: Optional[Logger] = None
    ) -> None:

        self.logger = logger or Logger(level=logging.INFO)
        self.scraper = scraper or NairametricsScraper(logger=self.logger)
        self.store = store or NewsStore(logger=self.logger)

    def get_new_items(
        self, scraped_news: Optional[NewsLike] = None
    ) -> NewsLike:

        scraped_news = scraped_news or self.scraper.scrape_category()
        if not scraped_news:
            raise Exception("Scraped news is empty or None!")

        stored_news = self.store.load() or []

        stored_links = {item["link"] for item in stored_news}

        new_items = [
            item for item in scraped_news
            if item["link"] not in stored_links
        ]

        return new_items
