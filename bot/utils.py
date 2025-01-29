from enum import Enum

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.Clients.user_storage import UserStorage
from config import Config


class MailingTypes(Enum):
    massive = "Общая"
    specified = "Заказавшим"


class ConfirmButtons(Enum):
    sure = "Уверен"


async def get_admin_ids() -> list:
    return set([int(el.strip()) for el in Config.ADMIN_IDS.split(",")])


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начать использование бота'),
        BotCommand(command='help', description='Помощь'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def mailing(bot: Bot, mailing_type: str, custom_type: str, mailing_message: str, buttons: list = None):
    if mailing_type == MailingTypes.massive.value:
        mailing_list = UserStorage.get_all_users_list()
    else:
        mailing_list = UserStorage.get_custom_users_list(custom_type)
    for i in await mailing_list:
        try:
            if buttons:
                await bot.send_message(
                    chat_id=i,
                    text=mailing_message,
                    reply_markup=make_keyboard(buttons)
                )
            else:
                await bot.send_message(
                    chat_id=i,
                    text=mailing_message,
                    reply_markup = ReplyKeyboardRemove()
                )
        except:
            pass

async def make_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
