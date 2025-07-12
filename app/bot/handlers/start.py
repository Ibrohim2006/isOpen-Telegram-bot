from aiogram.filters import Command
from app.bot.keyboards.reply import get_main_menu, get_user_type_menu
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Salom! Botimizga xush kelibsiz!\nIltimos kerakli bo‘limni tanlang 👇",
        reply_markup=get_main_menu()
    )


@start_router.message(F.text == "👤 Ro'yxatdan o'tish")
async def register_handler(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, ro'yxatdan o'tish turini tanlang:",
        reply_markup=get_user_type_menu()
    )
