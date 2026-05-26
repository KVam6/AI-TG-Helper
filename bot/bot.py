from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer 
from aiogram.utils.chat_action import ChatActionMiddleware

from utils.logger import logger
from bot.handlers import router
from config import WORKER_URL, BOT_TOKEN

async def main():
    api_server = TelegramAPIServer.from_base(WORKER_URL) # Using CloudFlare worker to bypass the restrictions in Russia
    session = AiohttpSession(api=api_server)

    bot = Bot(token=BOT_TOKEN, session=session) # Setting up our bot
    dp = Dispatcher()

    dp.include_router(router) # Include handlers from file
    logger.info("✅ Bot is working!")
    await dp.start_polling(bot)