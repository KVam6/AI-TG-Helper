from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WORKER_URL = "https://my-tg-bot-proxy.suslokat.workers.dev" # To bypass the locks

PROMPTS = { # For fufture
    "fast": "Отвечай коротко и точно",
    "detailed": "Отвечай подробно, с примерами"
}