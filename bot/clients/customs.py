import datetime

import gspread
import pandas as pd

from bot.Clients.user_storage import UserStorage
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

    async def add_custom_types_to_work(self, custom_type: str):
        pass

    async def get_custom_types_in_work(self):
        pass

    async def make_start_custom_message(self, custom_type: str, expected_date: str):
        # todo
        start_custom_message = (
            f"Заказ {custom_type}\n"
            f"Ожидаем {expected_date}\n"
            f"Колбасы и цены"
        )
        return start_custom_message

    async def make_custom_worksheet(self, custom_type: str):
        worksheet = self.client.worksheet(f"{Config.CUSTOM_PRICE_WORKSHEET_PREFIX}_{custom_type}")
        df = pd.DataFrame(worksheet.get_all_records())

        today = datetime.date.today().strftime("%d-%m-%Y")
        new_worksheet = self.client.add_worksheet(
            title=f"{custom_type}_{today}",
            rows=len(df) + 1,
            cols=len(UserStorage.get_all_users_list())
        )
        new_worksheet.update([df.columns.values.tolist()] + df.values.tolist())


gs_client = CustomsClient()

if __name__ == "__main__":
    gs_client = CustomsClient()
    print(gs_client.make_custom_worksheet("Вего"))
