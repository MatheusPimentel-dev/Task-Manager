import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramService:    
    @staticmethod
    def send_message(text):
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

        if not TOKEN or not CHAT_ID:
            return False

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": text
        }

        try:
            response = requests.post(url, data=data, timeout=10)
            return response.ok
        except requests.RequestException:
            return False

