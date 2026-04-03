

# store.py

import logging
from pipeline.aliases import NewsLike
from typing import Optional
from haashi_pkg.utility import Logger, FileHandler


class NewsStore:

    def __init__(
        self,
        path: Optional[str] = None,
        logger: Optional[Logger] = None,
        handler: Optional[FileHandler] = None

    ) -> None:
        self.path = path or "saved_news/news.json"
        self.logger = logger or Logger(level=logging.INFO)
        self.handler = handler or FileHandler(logger=self.logger)
        self.script_dir = self.handler.get_script_dir()
        self.news = []

    def _validate_news(self, news: Optional[NewsLike] = None) -> NewsLike:
        return news or []

    def load(self) -> NewsLike:
        path = str(self.script_dir / self.path)
        try:
            self.news = self.handler.read_json(path)
        except Exception as e:
            self.logger.error(f"Failed to load news: {e}")
            self.logger.error(exception=e, save_to_json=True)
            self.news = []
        return self._validate_news(self.news)  # type: ignore

    def save(self) -> None:
        path = str(self.script_dir / self.path)
        self.handler.save_json(data=self.news, path=path)
