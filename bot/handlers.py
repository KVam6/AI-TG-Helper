from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command

from bot.states import Model
import bot.keyboards as kb 

router = Router()

# COMMANDS
@router.message(CommandStart()) # Handle /start
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f"Привет, это твои персональный ИИ помощник!\nВыбери режим работы (его можно изменить в любой момент) и давай начнем", 
                         reply_markup=kb.start_keyboard)
    await state.set_state(Model.ChoosingModel)

# @router.message(Command('help')) # Handle /help
# async def cmd_start(message: Message):
#     await message.answer("no help here", reply_markup=kb.catalog) # Adding the keyboard

# STATES
# ---Choosing Model---
@router.message(Model.ChoosingModel, F.text == kb.buttons_text["FastMode"])
async def Model_name(message: Message, state: FSMContext):
    await state.update_data(name="FastMode")
    data = await state.get_data()
    await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")
    await state.set_state(Model.WaitingForRequest)

@router.message(Model.ChoosingModel, F.text == kb.buttons_text["ExpertMode"])
async def Model_name(message: Message, state: FSMContext):
    await state.update_data(name="ExpertMode")
    data = await state.get_data()
    await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")
    await state.set_state(Model.WaitingForRequest)

@router.message(Model.ChoosingModel)
async def Model_name(message: Message, state: FSMContext):
    await message.answer(f"Выбери режим работы используя кнопки",
                         reply_markup=kb.start_keyboard)

# ---Waiting For Request---
@router.message(Model.WaitingForRequest, F.text == kb.buttons_text["FastMode"])
async def Model_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["name"] == "FastMode":
        await message.answer(f"{data["name"]} уже выбран, можешь писать свой запрос!")
    else:
        await state.update_data(name="FastMode")
        data = await state.get_data()
        await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")

@router.message(Model.WaitingForRequest, F.text == kb.buttons_text["ExpertMode"])
async def Model_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["name"] == "ExpertMode":
        await message.answer(f"{data["name"]} уже выбран, можешь писать свой запрос!")
    else:
        await state.update_data(name="ExpertMode")
        data = await state.get_data()
        await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")

@router.message(Model.WaitingForRequest)
async def Model_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"запрос к {data["name"]}")

# OTHER
@router.message() # Handle everything
async def echo(message: Message, state: FSMContext):
    await message.answer(f"Ты не должен был сюда попасть, перезапусти бота /start")