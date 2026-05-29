from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command
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

            # Telegram показывает статус около 5 сек
            await asyncio.sleep(4)

    except asyncio.CancelledError:
        pass


# =========================
# COMMANDS
# =========================
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "👋 Привет!\n\n"
        "Я твой персональный ИИ-помощник.\n"
        "Могу отвечать на вопросы, помогать с текстами, объяснять темы и искать идеи.\n\n"
        "👇 Сначала выбери режим работы.\n"
        "Его можно поменять в любой момент:",
        reply_markup=kb.start_keyboard
    )

    await state.set_state(Model.ChoosingModel)


# =========================
# CHOOSING MODEL
# =========================
@router.message(Model.ChoosingModel, F.text == kb.buttons_text["FastMode"])
async def choose_fast(message: Message, state: FSMContext):
    await state.update_data(
        name="FastMode",
        history=[]
    )

    await message.answer(
        "⚡ Режим «Быстрый» включён.\n\n"
        "Я буду отвечать быстрее и короче.\n"
        "Отправь свой вопрос 👇"
    )

    await state.set_state(Model.WaitingForRequest)


@router.message(Model.ChoosingModel, F.text == kb.buttons_text["DetailedMode"])
async def choose_detailed(message: Message, state: FSMContext):
    await state.update_data(
        name="DetailedMode",
        history=[]
    )

    await message.answer(
        "🧠 Режим «Подробный» включён.\n\n"
        "Я буду отвечать подробнее и глубже.\n"
        "Отправь свой вопрос 👇"
    )

    await state.set_state(Model.WaitingForRequest)


@router.message(Model.ChoosingModel)
async def choose_model_invalid(message: Message):
    await message.answer(
        "👇 Пожалуйста, выбери режим с помощью кнопок ниже:",
        reply_markup=kb.start_keyboard
    )


# =========================
# WAITING FOR REQUEST
# =========================
@router.message(Model.WaitingForRequest, F.text == kb.buttons_text["FastMode"])
async def switch_fast(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["name"] == "FastMode":
        await message.answer(
            "⚡ Уже выбран режим «Быстрый».\n"
            "Можешь отправлять запрос 👇"
        )
    else:
        await state.update_data(name="FastMode")

        await message.answer(
            "⚡ Переключил на режим «Быстрый».\n"
            "Следующий ответ будет быстрее и короче."
        )


@router.message(Model.WaitingForRequest, F.text == kb.buttons_text["DetailedMode"])
async def switch_detailed(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["name"] == "DetailedMode":
        await message.answer(
            "🧠 Уже выбран режим «Подробный».\n"
            "Можешь отправлять запрос 👇"
        )
    else:
        await state.update_data(name="DetailedMode")

        await message.answer(
            "🧠 Переключил на режим «Подробный».\n"
            "Следующий ответ будет более развёрнутым."
        )


@router.message(Model.WaitingForRequest)
async def handle_request(message: Message, state: FSMContext):
    async with chat_locks[message.chat.id]:
        data = await state.get_data()

        history = data.get("history", [])

        # сохраняем сообщение пользователя
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
                "⏳ Ответ занял слишком много времени.\n"
                "Попробуй отправить сообщение ещё раз."
            )
            return

        except Exception as e:
            print(e)

            await message.reply(
                "⚠️ Не получилось получить ответ.\n"
                "Попробуй ещё раз через пару секунд."
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
                "⚠️ Модель не смогла ответить.\n"
                "Попробуй отправить запрос ещё раз."
            )
            return

        text = completion.choices[0].message.content

        # обновляем историю
        data = await state.get_data()
        history = data.get("history", [])

        history.append(
            {
                "role": "assistant",
                "content": text,
            }
        )

        # ограничиваем размер
        history = history[-20:]

        await state.update_data(history=history)

        # отправляем ответ
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


# =========================
# FALLBACK
# =========================
@router.message()
async def echo(message: Message):
    await message.answer(
        "Что-то пошло не так 😅\n\n"
        "Нажми /start и начнём заново."
    )