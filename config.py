from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN")
    ADMIN_IDS = getenv("ADMIN_IDS")
    USERS_FILE = "users.txt"

