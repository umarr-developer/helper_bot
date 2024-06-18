from aiogram import Router

from src.filters import PrivateTypeFilter
from src.handlers.private import admin, user
from src.middlewares import UserMiddleware

router = Router()
router.message.filter(PrivateTypeFilter())
router.message.middleware(UserMiddleware())
router.callback_query.middleware(UserMiddleware())
router.include_router(admin.router)
router.include_router(user.router)
