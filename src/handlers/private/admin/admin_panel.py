from aiogram import types, Router
from aiogram.filters import Command, StateFilter

router = Router()


@router.message(Command(commands=['admin']), StateFilter(None))
async def on_admin_panel(message: types.Message):
    text = '↘️ Панель администратора'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='👨‍🔧 Управление операторами',
                                           callback_data='admin-manage-operators')
            ],
            [
                types.InlineKeyboardButton(text='👨‍💼 Пользователи',
                                           callback_data='admin-manage-users'),
                types.InlineKeyboardButton(text='❓ Вопросы FAQ',
                                           callback_data='admin-manage-faq')
            ],
            [
                types.InlineKeyboardButton(text='⚙️ Настройки',
                                           callback_data='admin-settings'),
                types.InlineKeyboardButton(text='📊 Статистика',
                                           callback_data='admin-statistic')
            ],
            [
                types.InlineKeyboardButton(text='↩️ Перейти в панель пользователя',
                                           callback_data='admin-to-user-panel')
            ]
        ]
    )

    await message.answer(text, reply_markup=keyboard)
