import unittest
from unittest.mock import Mock, patch

import requests

from app.services.telegram_service import TelegramService


class TelegramServiceTestCase(unittest.TestCase):
    @patch.dict("os.environ", {"TELEGRAM_TOKEN": "", "TELEGRAM_CHAT_ID": ""}, clear=True)
    @patch("app.services.telegram_service.requests.post")
    def test_does_not_send_without_config(self, post):
        self.assertFalse(TelegramService.send_message("teste"))
        post.assert_not_called()

    @patch.dict("os.environ", {"TELEGRAM_TOKEN": "token", "TELEGRAM_CHAT_ID": "chat"}, clear=True)
    @patch("app.services.telegram_service.requests.post", side_effect=requests.RequestException)
    def test_returns_false_on_network_error(self, _post):
        self.assertFalse(TelegramService.send_message("teste"))

    @patch.dict("os.environ", {"TELEGRAM_TOKEN": "token", "TELEGRAM_CHAT_ID": "chat"}, clear=True)
    @patch("app.services.telegram_service.requests.post")
    def test_sends_expected_payload(self, post):
        post.return_value = Mock(ok=True)

        self.assertTrue(TelegramService.send_message("teste"))

        post.assert_called_once_with(
            "https://api.telegram.org/bottoken/sendMessage",
            data={"chat_id": "chat", "text": "teste"},
            timeout=10,
        )


if __name__ == "__main__":
    unittest.main()
