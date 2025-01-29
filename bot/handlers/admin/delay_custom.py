from aiogram import F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.clients.customs import gs_client
from bot.handlers.admin.init_handler import admin_router
from bot.states import Delay
from bot.texts import DELAY_MESSAGE
from bot.utils import make_keyboard, mailing, MailingTypes, ConfirmButtons


@admin_router.message(
    Delay.confirm,
    F.text.in_([el.value for el in ConfirmButtons])
)
async def confirm(msg: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    custom_type = user_data.get("custom_type")
    mailing_message = user_data.get("mailing_message")
    mailing_type = MailingTypes.specified.value

    await mailing(bot, mailing_type, custom_type, mailing_message)
    await msg.answer(text=f"Рассылка завершена", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@admin_router.message(
    Delay.expected_date,
)
async def expected_date_inserted(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    custom_type = user_data.get("custom_type")
    expected_date = msg.text.lower()
    mailing_message = DELAY_MESSAGE.format(
        custom_type=custom_type,
        expected_date=expected_date
    )
    await state.update_data(
        expected_date=expected_date,
        mailing_message=mailing_message
    )
    await msg.answer(
        text=f"Вы уверены, что хотите отправить данное сообщение?\n"
             f"Закупка - {custom_type}\n"
             f"Сообщение - {mailing_message}",
        reply_markup=await make_keyboard([el.value for el in ConfirmButtons])
    )
    await state.set_state(Delay.confirm)


@admin_router.message(
    Delay.custom_type,
)
async def custom_type_chosen(msg: Message, state: FSMContext):
    custom_type = msg.text.lower()
    await state.update_data(custom_type=custom_type)
    await msg.answer(text="Теперь, пожалуйста, введите дату предполагаемой закупки")
    await state.set_state(Delay.expected_date)

@admin_router.message(StateFilter(None), Command("delay_custom"))
async def delay_custom_handler(msg: Message, state: FSMContext):
    await msg.answer(
        text="Выберите вид закупки:",
        reply_markup=await make_keyboard(await gs_client.get_custom_types_in_work())
    )
    await state.set_state(Delay.custom_type)
