from aiogram import Router, types, F
from aiogram.filters import Command

from src.keyboards.list_keyboard import FAQListKeyboard
from src.models.questions import Question

router = Router()


@router.message(Command(commands=['/faq']))
@router.message(F.text == '❓ FAQ')
@router.callback_query(F.data.startswith('faq-action'))
async def on_faq(message: types.Message | types.CallbackQuery, db):
    buttons = await FAQListKeyboard.get_buttons(db, 'faq-question')

    text = 'Информация'
    keyboard = FAQListKeyboard(buttons, 'faq-action')

    if isinstance(message, types.CallbackQuery):
        await message.answer()

        prefix, index = message.data.split('_')
        await message.message.edit_text(text, reply_markup=keyboard.as_keyboard(int(index)))
        return

    await message.answer(text, reply_markup=keyboard.as_keyboard(0))


@router.callback_query(F.data.startswith('faq-question'))
async def on_faq_question(callback: types.CallbackQuery, db):
    await callback.answer()
    
    prefix, _id = callback.data.split('_')
    question: tuple[Question] = await Question.get(db, int(_id))

    text = question[0].answer
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Назад', callback_data='faq-action_0')
            ]
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard)
