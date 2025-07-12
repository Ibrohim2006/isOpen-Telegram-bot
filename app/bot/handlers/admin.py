from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.reply import get_main_menu

admin_router = Router()


@admin_router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Asosiy menyu:",
        reply_markup=get_main_menu()
    )
