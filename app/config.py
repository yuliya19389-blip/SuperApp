import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Получи ключ здесь: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = int(os.getenv("PORT", 8080))

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Не установлены TELEGRAM_TOKEN или GEMINI_API_KEY")
