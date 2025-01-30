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
    user_purchases = fields.JSONField(default=list)

    async def add_user_purchase(self, user_purchase: dict):
        self.user_purchases.append(user_purchase)
        await self.save()


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
        await Tortoise.get_connection("default").execute_script("PRAGMA journal_mode=WAL;")
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
        records = await CustomsWork.filter(custom_type=custom_type).values_list("user_purchases", flat=True)
        return [list(record.keys())[0] for record in records]

    @staticmethod
    async def save_user_to_working_custom_type(custom_type: str, user_purchase: dict):
        custom_obj = await CustomsWork.get(custom_type=custom_type)
        await custom_obj.add_user_purchase(user_purchase)

        logger.info(f"Пользователь {list(user_purchase.keys())[0]} добавлен в закупку {custom_type}")

    @staticmethod
    async def delete_custom_type_from_working(custom_type: str):
        await CustomsWork.filter(custom_type=custom_type).delete()
        logger.info(f"Закупка {custom_type} завершена")
