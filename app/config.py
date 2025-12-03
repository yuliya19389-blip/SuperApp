import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = int(os.getenv("PORT", 8080))

if not BOT_TOKEN or not CLAUDE_API_KEY:
    raise ValueError("Не установлены TELEGRAM_TOKEN или CLAUDE_API_KEY")
