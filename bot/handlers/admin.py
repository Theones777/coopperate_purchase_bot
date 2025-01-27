from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.Clients.user_storage import UserStorage
from bot.middlewares.check_access import CheckAccessMiddleware

admin_router = Router()
admin_router.message.middleware(CheckAccessMiddleware())


@admin_router.message(Command("start_custom"))
async def start_custom_handler(msg: Message):
    # todo start custom
    await msg.answer("Заглушка - начать заказ")


@admin_router.message(Command("delay_custom"))
async def delay_custom_handler(msg: Message):
    # todo delay custom
    # todo admin write when it coming
    await msg.answer("Заглушка - заказ задерживается")


@admin_router.message(Command("ready_custom"))
async def ready_custom_handler(msg: Message):
    # todo ready custom
    await msg.answer("Заглушка - заказ готов")


@admin_router.message(Command("message_mailing"))
async def message_mailing_handler(msg: Message, bot: Bot):
    # todo message_mailing
    for i in await UserStorage.get_users_list():
        try:
            await bot.send_message(chat_id=i,
                                   text='Это рассылка')
        except:
            pass
