from aiogram import types, F, Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['operator_menu']))
async def on_operator_menu(message: types.Message):
    text = 'Вы оператор'
    await message.answer(text)
