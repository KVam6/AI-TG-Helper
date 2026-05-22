from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command

from bot.states import Reg
import bot.keyboards as kb 

router = Router()

# COMMANDS
@router.message(CommandStart()) # Handle /start
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("YaY\nIt's registration time!!!", 
                         reply_markup=ReplyKeyboardRemove()) # Removing the keyboard
    await state.set_state(Reg.name)

@router.message(Command('help')) # Handle /help
async def cmd_start(message: Message):
    await message.answer("no help here", reply_markup=kb.catalog) # Adding the keyboard

# STATES
@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Now it's phone contact time",reply_markup=kb.get_contact)
    await state.set_state(Reg.contact)

@router.message(Reg.contact, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"U did it, ur name is {data['name']} and phone is {data['contact']}", reply_markup= ReplyKeyboardRemove())
    await state.clear()

@router.message(Reg.contact)
async def reg_contact(message: Message, state: FSMContext):
    await message.answer("Use the button")



# OTHER
@router.message(F.photo) # Handle any photo
async def cmd_photo(message: Message):
    await message.answer(f"Photo not allowed, id = {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[1].file_id)

@router.message(F.text == 'button1') # Handle text 
async def cmd_hi(message: Message):
    await message.answer(f"hi")

@router.callback_query(F.data.startswith("cbd_")) # Looking for "tag" "cbd_"
async def check_callback(callback: CallbackQuery):
    cb = callback.data.split('_')[1] # Using something like "tag" and getting it's text
    await callback.answer(f'close Callback {cb}', show_alert=True) # Text in mid of the screen
    await callback.message.answer("Ur first callback!")

@router.message() # Handle everything
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)