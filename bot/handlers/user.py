from aiogram import Router
from aiogram.types import Message

from bot.middlewares.check_user_access import CheckUserAccessMiddleware

user_router = Router()
user_router.message.middleware(CheckUserAccessMiddleware())


@user_router.message()
async def message_handler(msg: Message):
    await msg.answer(f"User_handler")
