

# formatter.py

from datetime import datetime
from typing import Dict


class NewsFormatter:

    PREFIX = "🚨 Just in:"
    LINK_TEXT = "👉 Full story:"

    @classmethod
    def format(cls, news_item: Dict[str, str]) -> str:
        dt = datetime.fromisoformat(news_item["timestamp"])
        formatted_date = dt.strftime("%b %d, %Y %I:%M %p")

        return (
            f"\n{cls.PREFIX}\n\n"
            f"{news_item['title']}\n\n"
            f"📅 {formatted_date}\n"
            f"{cls.LINK_TEXT} {news_item['link']}"
        )
