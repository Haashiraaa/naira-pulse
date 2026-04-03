

# telegram.py

import logging
import requests
from typing import Optional, Dict, Union
from haashi_pkg.utility import Logger


class NewsTelegramBot:

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        logger: Optional[Logger] = None
    ) -> None:

        self.logger = logger or Logger(level=logging.INFO)
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(
        self,
        message: str,
        item: Dict[str, Union[str, None]],
    ) -> None:

        payload: Dict[str, Union[str, None]] = {
            "chat_id": self.chat_id,
            "photo": item.get("image"),  # scraped image URL
            "caption": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(self.api_url, data=payload)
            self.logger.debug(f"Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message: {e}")
            self.logger.error(exception=e, save_to_json=True)
