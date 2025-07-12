from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
    ]
    await bot.set_my_commands(commands)
