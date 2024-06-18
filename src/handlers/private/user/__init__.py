from aiogram import Router

from src.handlers.private.user import start, menu, about, faq
from src.middlewares import ThrottlingMiddleware

router = Router()
router.message.middleware(ThrottlingMiddleware())
router.include_router(start.router)
router.include_router(menu.router)
router.include_router(about.router)
router.include_router(faq.router)
