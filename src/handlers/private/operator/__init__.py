from aiogram import Router
from src.handlers.private.operator import menu
from src.filters.chat import OperatorFilter
router = Router()

router.message.filter(OperatorFilter())
router.include_router(menu.router)