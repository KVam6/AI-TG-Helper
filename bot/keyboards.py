from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton, InlineKeyboardMarkup)

buttons_text = {
    "FastMode" : "Режим только ответы",
    "DetailedMode" : "Режим полное объяснение"
}

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons_text["FastMode"]), KeyboardButton(text=buttons_text["DetailedMode"])]
    ],
    resize_keyboard=True
)