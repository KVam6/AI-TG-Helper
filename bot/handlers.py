from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("YaY")

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer("no help here")

@router.message(F.photo)
async def cmd_photo(message: Message):
    await message.answer(f"Photo not allowed, id = {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[1].file_id)

@router.message(F.text == 'Привет')
async def cmd_hi(message: Message):
    await message.answer(f"hi")


@router.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)