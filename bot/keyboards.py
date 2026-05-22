from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton, InlineKeyboardMarkup)

menu = ReplyKeyboardMarkup( # Large buttons under your keyboard
    keyboard=[
        [KeyboardButton(text="button1")], # When pressed, it just send button's text to the chat
        [KeyboardButton(text="button2"), KeyboardButton(text="button3")]
    ],
    resize_keyboard=True,
    input_field_placeholder='Pick smth'
)

catalog = InlineKeyboardMarkup( # Buttons under message
    inline_keyboard=[
        [InlineKeyboardButton(text="url",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")], # When pressed, it execute argument
        [InlineKeyboardButton(text="callback_1",callback_data='cbd_1'),
          InlineKeyboardButton(text="callback_2",callback_data='cbd_2')]
    ]
)