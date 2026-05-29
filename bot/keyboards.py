from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

buttons_text = {
    "FastMode": "⚡ Быстрый ответ",
    "DetailedMode": "🧠 Подробное объяснение",
}

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=buttons_text["FastMode"]
            )
        ],
        [
            KeyboardButton(
                text=buttons_text["DetailedMode"]
            )
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери режим 👇",
)