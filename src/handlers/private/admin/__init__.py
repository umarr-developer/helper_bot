from aiogram import Router

from src.filters import AdminFilter
from src.handlers.private.admin import start, admin_panel, faq, cancel, manage_users

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())
router.include_router(start.router)
router.include_router(admin_panel.router)
router.include_router(faq.router)
router.include_router(cancel.router)
router.include_router(manage_users.router)
