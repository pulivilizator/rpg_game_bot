from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot):
    menu = [
        BotCommand(command='/start', description='start bot'),
    ]

    await bot.set_my_commands(menu)
