from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # For future work with AI
WORKER_URL = os.getenv("WORKER_URL", "https://my-tg-bot-proxy.suslokat.workers.dev") # Using CloudFlare to bypass the locks,
                                                                                     # If you are going to use it by your own, you should override this

PROMPTS = { # For future
    "fast": "Отвечай коротко и точно",
    "detailed": "Отвечай подробно, с примерами"
}