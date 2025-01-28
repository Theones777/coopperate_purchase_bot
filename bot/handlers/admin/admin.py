from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.handlers.admin.init_handler import admin_router


@admin_router.message(StateFilter(None), Command(commands=["cancel"]))
async def cancel_handler(msg: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await msg.answer("Возврат к началу", reply_markup=ReplyKeyboardRemove())


@admin_router.message(Command("start_custom"))
async def start_custom_handler(msg: Message):
    # todo start custom
    await msg.answer("Заглушка - начать заказ")


@admin_router.message(Command("delay_custom"))
async def delay_custom_handler(msg: Message):
    # todo delay custom
    await msg.answer("Заглушка - заказ задерживается")


@admin_router.message(Command("ready_custom"))
async def ready_custom_handler(msg: Message):
    # todo ready custom
    await msg.answer("Заглушка - заказ готов")

