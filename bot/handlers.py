from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
import bot.keyboards as kb 

router = Router()

@router.message(CommandStart()) # Handle /start
async def cmd_start(message: Message):
    await message.answer("YaY", 
                         reply_markup=kb.menu) # Adding the keyboard

@router.message(Command('help')) # Handle /help
async def cmd_start(message: Message):
    await message.answer("no help here", reply_markup=kb.catalog)

@router.message(F.photo) # Handle any photo
async def cmd_photo(message: Message):
    await message.answer(f"Photo not allowed, id = {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[1].file_id)

@router.message(F.text == 'button1') # Handle text 
async def cmd_hi(message: Message):
    await message.answer(f"hi")

@router.callback_query(F.data == 'cbd')
async def check_callback(callback: CallbackQuery):
    await callback.answer('close Callback', show_alert=True) # Text in mid of the screen
    await callback.message.answer("Ur first callback!")

@router.message() # Handle everything
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)