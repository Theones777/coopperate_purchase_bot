from config import Config


class UserStorage:

    @staticmethod
    async def get_users_list() -> list:
        try:
            with open(Config.USERS_FILE, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            with open(Config.USERS_FILE, 'w') as f:
                f.write("")
            return []

    @staticmethod
    async def save_new_user(user_id: int):
        users_list = await UserStorage.get_users_list()
        if str(user_id) + '\n' not in users_list:
            with open(Config.USERS_FILE, 'a') as f:
                f.write(str(user_id) + '\n')
