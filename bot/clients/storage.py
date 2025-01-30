from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

from bot.log import logger
from config import Config


class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField()
    full_name = fields.CharField(max_length=255)
    tg_user_name = fields.CharField(max_length=255)


class CustomsWork(Model):
    id = fields.IntField(pk=True)
    custom_type = fields.CharField(max_length=255)


class Storage:

    def __init__(self):
        run_async(self.init_db())

    @staticmethod
    async def init_db():
        await Tortoise.init(
            db_url=Config.DB_URL,
            modules={"models": ["__main__"]}
        )
        await Tortoise.generate_schemas()
        logger.info(f"База данных проинициализирована")

    @staticmethod
    async def save_new_user(user_id: int, user_full_name: str, tg_user_name: str):
        user, created = await User.get_or_create(
            tg_id=user_id,
            defaults={
                "full_name": user_full_name,
                "tg_user_name": tg_user_name
            }
        )
        await Tortoise.close_connections()

        if created:
            logger.info(f"Новый пользователь {user_full_name} добавлен")
        else: # todo delete
            print("Пользователь уже существует")

    @staticmethod
    async def get_all_users_list() -> list:
        users = await User.all()
        await Tortoise.close_connections()

        return [user.tg_id for user in users]

    @staticmethod
    async def save_custom_type_to_work(custom_type: str):
        await CustomsWork.create(custom_type=custom_type)
        await Tortoise.close_connections()

        logger.info(f"Добавление заказа {custom_type} в работу")

    @staticmethod
    async def get_custom_types_in_work() -> list:
        custom_types = await CustomsWork.all()
        await Tortoise.close_connections()

        return [custom_type.custom_type for custom_type in custom_types]

    @staticmethod
    async def get_custom_users_list(custom_type: str) -> list:
        pass
