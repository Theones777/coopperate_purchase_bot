from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


admin_router = Router()


@admin_router.message(Command("start_custom"))
async def start_custom_handler(msg: Message):
    # todo start custom
    # todo only admins
    await msg.answer("Заглушка - начать заказ")


@admin_router.message(Command("delay_custom"))
async def delay_custom_handler(msg: Message):
    # todo delay custom
    # todo only admins
    # todo maybe admin write when it coming
    await msg.answer("Заглушка - заказ задерживается")
