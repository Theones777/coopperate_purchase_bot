from aiogram import Router
from aiogram.types import Message


user_router = Router()


@user_router.message()
async def message_handler(msg: Message):
    await msg.answer(f"User_handler")
