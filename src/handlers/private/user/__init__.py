from aiogram import Router

from src.filters.chat import UserFilter
from src.handlers.private.user import start, menu, about, faq
from src.middlewares import UserMiddleware, ThrottlingMiddleware

router = Router()
router.message.middleware(UserMiddleware())
router.message.middleware(ThrottlingMiddleware())
router.callback_query.middleware(UserMiddleware())
router.include_router(start.router)
router.include_router(menu.router)
router.include_router(about.router)
router.include_router(faq.router)
