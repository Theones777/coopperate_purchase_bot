from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN")
    ADMIN_IDS = getenv("ADMIN_IDS")
    GS_CONFIG = getenv("GS_CONFIG")
    GS_SHEET_NAME = getenv("GS_SHEET_NAME")
    USERS_FILE = "users.txt"
    CUSTOM_PRICE_WORKSHEET_PREFIX = "прайс"
