

# app.py


import logging
import sys
from pipeline.scraper import NairametricsScraper
from pipeline.store import NewsStore
from pipeline.processor import NewsProcessor
from pipeline.formatter import NewsFormatter
from haashi_pkg.utility import Logger
from typing import Optional, cast


def main(logger: Optional[Logger] = None) -> None:

    logger = logger or Logger(level=logging.INFO)

    scraper = NairametricsScraper(logger=logger)
    store = NewsStore(logger=logger)
    processor = NewsProcessor(scraper=scraper, store=store, logger=logger)

    scraped_news = processor.scraper.scrape_category()

    news = processor.get_new_items(scraped_news)

    for news_item in news:
        formatted_news = cast(str, NewsFormatter.format(news_item))
        logger.info(formatted_news)

    store.news = news
    store.save()


if __name__ == "__main__":
    main()
