from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter

router = Router()


@router.message(Command(commands=['about']), StateFilter(None))
@router.message(F.text == '☑️ О боте')
async def on_about(message: types.Message):
    text = 'Информация'
    await message.answer(text)
