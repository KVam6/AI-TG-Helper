from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer # <-- Импортируем из client.telegram

from config import WORKER_URL, BOT_TOKEN

# 1. Создаем объект TelegramAPIServer с вашим URL
api_server = TelegramAPIServer.from_base(WORKER_URL)

# 2. Передаем этот объект в сессию
session = AiohttpSession(api=api_server)

# 3. Передаем сессию в бота
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass