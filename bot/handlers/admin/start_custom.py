from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.handlers.admin.init_handler import admin_router


@admin_router.message(Command("start_custom"))
async def start_custom_handler(msg: Message):
    # todo start custom
    await msg.answer("Заглушка - начать заказ")