from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.models.questions import Question

router = Router()


class AddQuestionState(StatesGroup):
    question = State()
    answer = State()
    accept = State()


@router.callback_query(F.data == 'admin_manage_faq')
async def on_admin_faq(callback: types.CallbackQuery):
    text = 'Раздел с часто задаваемыми вопросами'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='➕ Добавить вопрос', callback_data='admin_add_question')
            ],
            [
                types.InlineKeyboardButton(text='📒 Перейти к списку', callback_data='admin_faq_list')
            ]
        ]
    )
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'admin_add_question')
async def on_admin_add_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.set_state(AddQuestionState.question)
    text = 'Введите вопрос'
    await callback.message.answer(text)


@router.message(AddQuestionState.question)
async def on_admin_add_question_state_question(message: types.Message, state: FSMContext):
    await state.set_state(AddQuestionState.answer)
    await state.update_data({'question': message.text})

    text = 'Введите ответ к вопросу'
    await message.answer(text)


@router.message(AddQuestionState.answer)
async def on_admin_add_question_state_answer(message: types.Message, state: FSMContext):
    await state.set_state(AddQuestionState.accept)
    await state.update_data({'answer': message.text})

    data = await state.get_data()
    text = 'Данные вопроса\n' \
           f'Вопрос: {data.get("question")}\n' \
           f'Ответ: {data.get("answer")}'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='✅ Сохранить', callback_data='admin_save_question'),
                types.InlineKeyboardButton(text='❌ Отмена', callback_data='admin_cancel')
            ]
        ]
    )

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'admin_save_question', AddQuestionState.accept)
async def on_admin_add_question_state_accept(callback: types.CallbackQuery, state: FSMContext, db):
    await callback.answer('Умпешно сохранен')
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    question = data.get('question')
    answer = data.get('answer')

    await Question.new(db, question, answer)

    text = 'Вопрос успешно сохранен'
    await callback.message.answer(text)

    await state.clear()
