from aiogram import F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.Clients.GS import gs_client
from bot.handlers.admin.init_handler import admin_router
from bot.states import Ready
from bot.texts import READY_MESSAGE
from bot.utils import make_keyboard, mailing, ConfirmButtons, MailingTypes


@admin_router.message(
    Ready.confirm,
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
    Ready.custom_type,
    F.text.in_(gs_client.get_custom_names_in_work())
)
async def custom_type_chosen(msg: Message, state: FSMContext):
    custom_type = msg.text.lower()
    mailing_message = READY_MESSAGE.format(custom_type=custom_type)
    await state.update_data(
        custom_type=custom_type,
        mailing_message=mailing_message
    )
    await msg.answer(
        text=f"Вы уверены, что хотите отправить данное сообщение?\n"
             f"Закупка - {custom_type}\n"
             f"Сообщение - {mailing_message}",
        reply_markup=make_keyboard([el.value for el in ConfirmButtons])
    )
    await state.set_state(Ready.confirm)


@admin_router.message(StateFilter(None), Command("ready_custom"))
async def ready_custom_handler(msg: Message, state: FSMContext):
    await msg.answer(
        text="Выберите вид закупки:",
        reply_markup=make_keyboard(gs_client.get_custom_names_in_work())
    )
    await state.set_state(Ready.custom_type)
