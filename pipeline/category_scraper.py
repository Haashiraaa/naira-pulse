

# category_scraper.py


import requests
import logging

from typing import List, Dict, cast, Optional
from haashi_pkg.utility import Logger


class NairametricsScraper:

    def __init__(self, logger: Optional[Logger] = None) -> None:

        self.URL = (
            "https://nairametrics.com"
            "/wp-json/wp/v2/posts?categories=207871&_embed"
        )

        self.headers: Dict[str, str] = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.logger = logger or Logger(level=logging.INFO)
        self.posts_list: List[Dict[str, str]] = []

    def scrape_category(self) -> Optional[List[Dict[str, str]]]:

        response: Optional[requests.Response] = None

        try:

            response = requests.get(url=self.URL, headers=self.headers)
            response.raise_for_status()
            self.logger.debug(f"Response: {response.status_code}")

        except requests.exceptions.Timeout:
            self.logger.error("Request timeout - site may be down")
            return

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch page: {e}")
            self.logger.error(exception=e, save_to_json=True)
            raise

        posts = response.json()
        if not posts:
            raise Exception("No posts found!")

        for post in posts:
            title = post["title"]["rendered"]
            link = post["link"]
            timestamp = post["date"]

            self.posts_list.append({
                "title": title, "link": link, "timestamp": timestamp
            })

        return self.posts_list


if __name__ == "__main__":
    scraper = NairametricsScraper()
    import json
    print(json.dumps(scraper.scrape_category(), indent=4))
