from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY") # I'm going to use OpenRouter
WORKER_URL = os.getenv("WORKER_URL", "https://my-tg-bot-proxy.suslokat.workers.dev") # Using CloudFlare to bypass the locks,
                                                                                     # If you are going to use it by your own, you should override this

PROMPTS = { 
    "fast": "Отвечай коротко и точно",
    "detailed": "Отвечай подробно, с примерами"
}