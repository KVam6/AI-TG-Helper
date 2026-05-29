from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
from aiogram import flags
from aiogram.enums.chat_action import ChatAction
from aiogram.utils.chat_action import ChatActionMiddleware
from collections import defaultdict
import asyncio


from ai.client import make_completion
from bot.states import Model
from utils.text_formatter import format_for_telegram, split_text
import bot.keyboards as kb 

router = Router()

# блокировка по chat_id
chat_locks = defaultdict(asyncio.Lock)

async def typing_loop(bot, chat_id: int):
    try:
        while True:
            await bot.send_chat_action(
                chat_id=chat_id,
                action="typing"
            )

            # Telegram держит статус ~5 сек
            await asyncio.sleep(4)

    except asyncio.CancelledError:
        pass

# COMMANDS
@router.message(CommandStart()) # Handle /start
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f"Привет, это твои персональный ИИ помощник!\nВыбери режим работы (его можно изменить в любой момент) и давай начнем", 
                         reply_markup=kb.start_keyboard)
    await state.set_state(Model.ChoosingModel)


# STATES
# ---Choosing Model---
@router.message(Model.ChoosingModel, F.text == kb.buttons_text["FastMode"])
async def Model_name(message: Message, state: FSMContext):
    await state.update_data(name="FastMode")
    data = await state.get_data()
    await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")
    await state.set_state(Model.WaitingForRequest)

@router.message(Model.ChoosingModel, F.text == kb.buttons_text["DetailedMode"])
async def Model_name(message: Message, state: FSMContext):
    await state.update_data(name="DetailedMode")
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

@router.message(Model.WaitingForRequest, F.text == kb.buttons_text["DetailedMode"])
async def Model_name(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["name"] == "DetailedMode":
        await message.answer(f"{data["name"]} уже выбран, можешь писать свой запрос!")
    else:
        await state.update_data(name="DetailedMode")
        data = await state.get_data()
        await message.answer(f"Прекрасно, выбран {data["name"]}, можешь писать свой запрос!")


@router.message(Model.WaitingForRequest)
async def Model_name(message: Message, state: FSMContext):
    async with chat_locks[message.chat.id]:
        data = await state.get_data()

        history = data.get("history", [])

        history.append(
            {
                "role": "user",
                "content": message.text,
            }
        )

        await state.update_data(history=history)

        typing_task = asyncio.create_task(
            typing_loop(
                message.bot,
                message.chat.id
            )
        )

        try:
            completion = await asyncio.wait_for(
                make_completion(
                    history,
                    data["name"],
                ),
                timeout=60
            )

        except asyncio.TimeoutError:
            await message.reply(
                "⚠️ Модель слишком долго отвечает."
            )
            return

        except Exception as e:
            print(e)

            await message.reply(
                "⚠️ Ошибка при обращении к модели."
            )
            return

        finally:
            typing_task.cancel()

            try:
                await typing_task
            except asyncio.CancelledError:
                pass

        if completion is None:
            await message.reply(
                "⚠️ Модель не ответила."
            )
            return

        text = completion.choices[0].message.content
        data = await state.get_data()

        history = data.get("history", [])

        history.append(
            {
                "role": "assistant",
                "content": text,
            }
        )

        await state.update_data(history=history)

        try:
            formatted = await format_for_telegram(text)

            for chunk in split_text(formatted):
                await message.reply(
                    chunk,
                    parse_mode="MarkdownV2"
                )

        except Exception:
            for chunk in split_text(text):
                await message.reply(chunk)

# OTHER
@router.message() # Handle everything
async def echo(message: Message, state: FSMContext):
    await message.answer(f"Ты не должен был сюда попасть, перезапусти бота /start")