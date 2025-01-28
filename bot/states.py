from aiogram.fsm.state import StatesGroup, State


class Mailing(StatesGroup):
    mailing_type = State()
    custom_type = State()
    mailing_message = State()
    confirm = State()
