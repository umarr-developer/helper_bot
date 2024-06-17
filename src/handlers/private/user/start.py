from aiogram import Router, types
from aiogram.filters import Command

from src.handlers.private.user.menu import menu
from src.models import User

router = Router()


@router.message(Command(commands=['start']))
async def on_start(message: types.Message, user: User, db):
    if not user:
        user_id = message.from_user.id
        await User.new(db, user_id=user_id)

        text = 'Добро пожаловать, новый пользователь'
        await message.answer(text)

    else:
        await menu(message)
