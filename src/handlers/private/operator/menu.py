from aiogram import types, F, Router
from aiogram.filters import Command, StateFilter
from sqlalchemy.orm import sessionmaker

from models import Operator

router = Router()


@router.message(Command(commands=['operator_menu']), StateFilter(None))
@router.callback_query(F.data.startswith('disable-operator'))
@router.callback_query(F.data.startswith('enable-operator'))
async def on_operator_menu(message: types.Message | types.CallbackQuery, db: sessionmaker):
    user_id = message.from_user.id

    if isinstance(message, types.CallbackQuery):
        prefix, user_id = message.data.split('_')
        user_id = int(user_id)

        if prefix == 'disable-operator':
            await Operator.disable(db, user_id)
        elif prefix == 'enable-operator':
            await Operator.enable(db, user_id)

    operator = await Operator.get(db, user_id)

    text = 'Меню оператора'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='🟢 Активный',
                    callback_data=f'disable-operator_{user_id}'
                )
                if operator[0].active else
                types.InlineKeyboardButton(
                    text='🔴 Неактивный',
                    callback_data=f'enable-operator_{user_id}'
                )
            ],
            [
                types.InlineKeyboardButton(
                    text=f'✉️ Тикеты ({3})',
                    callback_data='tickets'
                ),
                types.InlineKeyboardButton(
                    text=f'🛎️ Уведомления ({5})',
                    callback_data='notifications'
                )
            ],
            [
                types.InlineKeyboardButton(
                    text='📒 История',
                    callback_data='history'
                )
            ]
        ]
    )

    if isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.edit_reply_markup(reply_markup=keyboard)
        return

    await message.answer(text, reply_markup=keyboard)
