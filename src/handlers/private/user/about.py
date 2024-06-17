from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['about']))
@router.message(F.text == '☑️ О боте')
async def on_about(message: types.Message):
    text = 'Информация'
    await message.answer(text)
