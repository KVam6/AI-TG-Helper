from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer 

from bot.handlers import router
from config import WORKER_URL, BOT_TOKEN

async def main():
    api_server = TelegramAPIServer.from_base(WORKER_URL)
    session = AiohttpSession(api=api_server)

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)