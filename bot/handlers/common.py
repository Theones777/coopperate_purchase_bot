from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.clients.user_storage import UserStorage
from bot.texts import START_ADMIN_MESSAGE, START_USER_MESSAGE, HELP_MESSAGE
from bot.utils import get_admin_ids

common_router = Router()


@common_router.message(StateFilter(None), Command(commands=["start"]))
async def message_start_handler(msg: Message, state: FSMContext):
    await state.clear()

    user_id: int = msg.from_user.id
    admin_ids = await get_admin_ids()
    await UserStorage.save_new_user(user_id)

    if user_id in admin_ids:
        message = START_ADMIN_MESSAGE
    else:
        message = START_USER_MESSAGE
    await msg.answer(message, reply_markup=ReplyKeyboardRemove())


@common_router.message(Command("help"))
async def message_help_handler(msg: Message):
    await msg.answer(HELP_MESSAGE)


@common_router.message(Command("test"))
async def test_handler(msg: Message):
    from pprint import pprint
    pprint(msg)
    await msg.answer(f"Твой ID: {msg.from_user.id}")
