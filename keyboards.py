from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

btn_check_1 = KeyboardButton("Проверить Мерседес")
btn_check_2 = KeyboardButton("В007АН777")
greet_kb = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add(btn_check_1)
    .add(btn_check_2)
)
inline_btn_1 = InlineKeyboardButton("Остальная информация", callback_data="all")
inline_kb = InlineKeyboardMarkup().add(inline_btn_1)
