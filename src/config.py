import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    @staticmethod
    def validate():
        if not Config.BOT_TOKEN:
            raise ValueError("Telegram bot token not found in environment variables")
