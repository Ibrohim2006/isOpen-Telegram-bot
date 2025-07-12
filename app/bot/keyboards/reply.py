from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Ro'yxatdan o'tish")],
            [KeyboardButton(text="ℹ️ Ma'lumot")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_user_type_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Ish beruvchi"),
                KeyboardButton(text="Ishchi")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
