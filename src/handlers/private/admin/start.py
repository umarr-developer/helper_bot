from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from sqlalchemy.orm import sessionmaker

from src.models import User

router = Router()


@router.message(Command(commands=['start', 'help']), StateFilter(None))
async def on_start(message: types.Message, user: User, db: sessionmaker):
    if not user:
        user_id = message.from_user.id
        await User.new(db, user_id)
    text = 'Команды админинистратора:\n' \
           '/admin - панель администратора'
    await message.answer(text)
