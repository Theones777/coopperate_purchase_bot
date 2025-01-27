from config import Config


async def get_admin_ids() -> list:
    ids = [el.strip() for el in Config.ADMINS_IDS.split(",")]
    return ids
