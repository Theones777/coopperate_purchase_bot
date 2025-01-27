from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChatAdministrators

from config import Config


async def get_admin_ids() -> list:
    return set([int(el.strip()) for el in Config.ADMIN_IDS.split(",")])


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начать использование бота'),
        BotCommand(command='help', description='Помощь'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
