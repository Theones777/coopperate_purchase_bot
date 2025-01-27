from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


common_router = Router()


@common_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        "Привет! Я бот для проведения совместной закупки из <b>Bhajan Cafe</b>. "
        "При проведении новой закупки я отправлю Вам сообщение"
    )


@common_router.message(Command("test"))
async def message_handler(msg: Message):
    # some tests
    await msg.answer(f"Твой ID: {msg.from_user.id}")
