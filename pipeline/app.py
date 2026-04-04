

# app.py


import logging
import os
import time
from pipeline.scraper import NairametricsScraper
from pipeline.store import NewsStore
from pipeline.processor import NewsProcessor
from pipeline.formatter import NewsFormatter
from pipeline.telegram import NewsTelegramBot
from haashi_pkg.utility import Logger
from typing import Optional, Union


class NewsPipeline:

    def __init__(
        self,
        scraper: Optional[NairametricsScraper] = None,
        store: Optional[NewsStore] = None,
        logger: Optional[Logger] = None
    ) -> None:

        self.CHAT_ID = os.getenv("TG_CHAT_ID")
        self.BOT_TOKEN = os.getenv("TG_NEWS_BOT_TOKEN")

        self.logger = logger or Logger(level=logging.INFO)
        self.scraper = scraper or NairametricsScraper(logger=self.logger)
        self.store = store or NewsStore(logger=self.logger)

    def run(self, delay: Union[float, int] = 600):

        failed_attempts: int = 0

        while failed_attempts < 3:

            try:
                if not self.CHAT_ID or not self.BOT_TOKEN:
                    raise Exception("Telegram credentials not found!")

                bot = NewsTelegramBot(
                    bot_token=self.BOT_TOKEN,
                    chat_id=self.CHAT_ID,
                    logger=self.logger
                )

                processor = NewsProcessor(
                    scraper=self.scraper, store=self.store
                )

                scraped_news = self.scraper.fetch_financial_news()

                news = processor.get_new_items(scraped_news)
                news = news[::-1]

                for news_item in news:

                    formatted_news = NewsFormatter.format(news_item)
                    bot.send_message(formatted_news, news_item)
                    # self.logger.info(formatted_news)

                self.store.news = scraped_news
                self.store.save()

                self.logger.info("Sleeping for 600 seconds...")
                time.sleep(delay)

            except Exception as e:
                self.logger.error(f"Failed to process news: {e}")
                self.logger.error(exception=e, save_to_json=True)
                failed_attempts += 1
                retries = 3 - failed_attempts
                self.logger.info(f"Available retries: {retries}")
                self.logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
