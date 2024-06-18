from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import sessionmaker

from src.models import User

router = Router()


@router.message(Command(commands=['start']))
async def on_start(message: types.Message, user: User, db: sessionmaker):
    if not user:
        user_id = message.from_user.id
        await User.new(db, user_id)
    text = 'Админ панель'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Управление операторами', callback_data='manage_operators'),
                types.InlineKeyboardButton(text='Управление пользователями', callback_data='manage_users'),
            ],
            [
                types.InlineKeyboardButton(text='Статистика бота', callback_data='statistic_bot')
            ],
            [
                types.InlineKeyboardButton(text='Перейти в панель пользователя', callback_data='user_interface')
            ]
        ]
    )
    await message.answer(text, reply_markup=keyboard)
