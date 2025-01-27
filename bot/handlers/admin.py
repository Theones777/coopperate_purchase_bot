from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


admin_router = Router()


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
async def message_mailing_handler(msg: Message):
    # todo message_mailing
    await msg.answer("Заглушка - Рассылка всем")
