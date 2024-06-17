from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['menu']))
async def on_menu(message: types.Message):
    text = 'Вы главном меню'
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                types.KeyboardButton(text='🛎️ Поддержка'),
                types.KeyboardButton(text='📝 Отправить тикет')
            ],
            [
                types.KeyboardButton(text='❓ FAQ'),
                types.KeyboardButton(text='☑️ О боте')
            ]
        ]
    )
    await message.answer(text, reply_markup=keyboard)
