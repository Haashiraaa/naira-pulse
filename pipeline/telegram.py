

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
        self.msg_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        )
        self.img_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        )

    def send_message_without_image(self, message: str) -> None:

        payload: Dict[str, Union[str, None]] = {
            "chat_id": self.chat_id,
            "caption": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(self.msg_url, data=payload)
            self.logger.debug(f"Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message: {e}")
            self.logger.error(exception=e, save_to_json=True)

    def send_message_with_image(
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
            response = requests.post(self.img_url, data=payload)
            self.logger.debug(f"Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message: {e}")
            self.logger.error(exception=e, save_to_json=True)

    def send_message(
        self, message: str, item: Dict[str, Union[str, None]]
    ) -> None:

        if item.get("image"):
            self.send_message_with_image(message, item)
        else:
            self.send_message_without_image(message)
