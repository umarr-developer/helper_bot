from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter

from src.handlers.private.user.menu import on_menu
from src.models import User

router = Router()


@router.callback_query(F.data == 'admin_to_user_panel', StateFilter(None))
@router.message(Command(commands=['start']), StateFilter(None))
async def on_start(message: types.Message | types.CallbackQuery, user: User, db):
    if isinstance(message, types.CallbackQuery):
        message = message.message
        
    if not user:
        user_id = message.from_user.id
        await User.new(db, user_id=user_id)

        text = 'Добро пожаловать, новый пользователь'
        await message.answer(text)

    else:
        await on_menu(message)
