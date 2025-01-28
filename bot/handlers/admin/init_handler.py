from aiogram import Router

from bot.middlewares.check_access import CheckAccessMiddleware

admin_router = Router()
admin_router.message.middleware(CheckAccessMiddleware())
