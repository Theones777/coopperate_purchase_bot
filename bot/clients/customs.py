import datetime

import gspread
import pandas as pd

from bot.log import logger
from bot.texts import START_CUSTOM_MESSAGE
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

    async def make_custom_body(self, custom_type):
        custom_body = ""
        worksheet = self.client.worksheet(f"{Config.CUSTOM_PRICE_WORKSHEET_PREFIX}_{custom_type}")
        df = pd.DataFrame(worksheet.get_all_records())
        for i in range(len(df)):
            if df.iloc[i, 2] == "да":
                custom_body += f"{df.iloc[i, 0]} - {df.iloc[i, 1]} рублей\n"
        return custom_body

    async def make_start_custom_message(self, custom_type: str, expected_date: str):
        application_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        custom_body = await self.make_custom_body(custom_type)
        start_custom_message = START_CUSTOM_MESSAGE.format(
            custom_type=custom_type,
            expected_date=expected_date,
            application_date=application_date,
            custom_body=custom_body
        )

        logger.info(f"Сообщение для закупки {custom_type} сформировано")
        return start_custom_message

    async def make_custom_worksheet(self, custom_type: str):
        worksheet = self.client.worksheet(f"{Config.CUSTOM_PRICE_WORKSHEET_PREFIX}_{custom_type}")
        df = pd.DataFrame(worksheet.get_all_records())
        df.drop(columns=Config.AVAILABLE_COLUMN_NAME, inplace=True)
        df = df.transpose()
        df["Итого"] = [0 for _ in range(len(df))]

        today = datetime.date.today().strftime("%d-%m-%Y")
        new_worksheet = self.client.add_worksheet(
            title=f"{custom_type}_{today}",
            rows=len(df) + 1,
            cols=2000
        )
        new_worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        logger.info(f"Создана новая страница для заказа {custom_type}")
