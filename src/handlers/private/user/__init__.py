from aiogram import Router

from src.handlers.private.user import start, menu, about, faq
from src.middlewares import ThrottlingMiddleware, BlockedUserMiddleware

router = Router()
router.message.middleware(ThrottlingMiddleware())
router.message.middleware(BlockedUserMiddleware())
router.include_router(start.router)
router.include_router(menu.router)
router.include_router(about.router)
router.include_router(faq.router)
