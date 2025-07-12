import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.bot.handlers.admin import admin_router
from app.bot.handlers.start import start_router
from app.bot.handlers.employee import employee_router
from app.bot.handlers.employer import employer_router
from dotenv import load_dotenv
from app.core.commands import set_bot_commands
from app.database.base import init_db

load_dotenv()
init_db()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(employee_router)
    dp.include_router(employer_router)
    dp.include_router(admin_router)

    await set_bot_commands(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
