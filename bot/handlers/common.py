from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.Clients.user_storage import UserStorage
from bot.utils import get_admin_ids

common_router = Router()


@common_router.message(Command("start"))
async def message_start_handler(msg: Message):
    user_id: int = msg.from_user.id
    admin_ids = await get_admin_ids()
    await UserStorage.save_new_user(user_id)

    if user_id in admin_ids:
        await msg.answer(
            "Привет! У Вас есть права администратора!\n"
            "Команды, доступные администратору:\n "
            "/start_custom - Начать закупку,\n "
            "/delay_custom - Заказ задерживается,\n "
            "/ready_custom - Заказ готова к выдаче,\n "
            "/message_mailing - Отправка всем сообщения"
        )
    else:
        await msg.answer(
            "Привет! Я бот для проведения совместной закупки из <b>Bhajan Cafe</b>. "
            "При проведении новой закупки я отправлю Вам сообщение"
        )


@common_router.message(Command("help"))
async def message_help_handler(msg: Message):
    await msg.answer("Номер для связи - +7 123 456789 Шурик")   # Todo help message


@common_router.message(Command("test"))
async def test_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
