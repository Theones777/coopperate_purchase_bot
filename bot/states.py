from aiogram.fsm.state import StatesGroup, State


class Mailing(StatesGroup):
    mailing_type = State()
    custom_type = State()
    mailing_message = State()
    confirm = State()


class Ready(StatesGroup):
    custom_type = State()
    confirm = State()


class Delay(StatesGroup):
    custom_type = State()
    expected_date = State()
    confirm = State()
