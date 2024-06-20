from aiogram import F, types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['cancel']))
@router.callback_query(F.data == 'admin_cancel')
async def on_admin_cancel(message: types.Message | types.CallbackQuery):
    if isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.edit_reply_markup()

        message = message.message

    text = 'Действие отменено'
    await message.answer(text)
