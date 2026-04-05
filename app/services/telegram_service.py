import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramService:    
    @staticmethod
    def send_message(text):
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": text
        }
        requests.post(url, data=data)


