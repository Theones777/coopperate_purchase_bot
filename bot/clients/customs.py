import datetime

import gspread
import pandas as pd

from bot.clients.init_clients import storage_client
from bot.clients.storage import Storage
from bot.log import logger
from config import Config


class CustomsClient:
    def __init__(self):
        self.client = gspread.service_account(filename=Config.GS_CONFIG).open(Config.GS_SHEET_NAME)

    async def get_all_custom_types(self):
        worksheet_list = self.client.worksheets()
        custom_types = [
            el.title.replace(f"{Config.CUSTOM_PRICE_WORKSHEET_PREFIX}_", "") for el in worksheet_list
            if el.title.startswith(Config.CUSTOM_PRICE_WORKSHEET_PREFIX)]
        return custom_types

    @staticmethod
    async def add_custom_types_to_work(custom_type: str):
        await storage_client.save_custom_type_to_work(custom_type)

    @staticmethod
    async def get_custom_types_in_work():
        return await storage_client.get_custom_types_in_work()

    async def make_start_custom_message(self, custom_type: str, expected_date: str):
        start_custom_message = (
            f"Заказ {custom_type}\n"
            f"Ожидаем {expected_date}\n"
            f"Колбасы и цены"
        )
        logger.info(f"Сообщение для заказа {custom_type} сформировано")
        return start_custom_message

    async def make_custom_worksheet(self, custom_type: str):
        worksheet = self.client.worksheet(f"{Config.CUSTOM_PRICE_WORKSHEET_PREFIX}_{custom_type}")
        df = pd.DataFrame(worksheet.get_all_records())

        today = datetime.date.today().strftime("%d-%m-%Y")
        new_worksheet = self.client.add_worksheet(
            title=f"{custom_type}_{today}",
            rows=len(df) + 1,
            cols=2000
        )
        new_worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        logger.info(f"Создана новая страница для заказа {custom_type}")
