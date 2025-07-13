from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Ro'yxatdan o'tish")],
            [KeyboardButton(text="ℹ️ Admin panel")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_user_type_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👔 Ish beruvchi")],
            [KeyboardButton(text="👷‍♂️ Ishchi")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👔 Ish beruvchi")],
            [KeyboardButton(text="👷 Ishchi")],
            [KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True
    )
    return keyboard
