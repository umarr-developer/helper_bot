import asyncio

from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from src.keyboards import FAQListKeyboard
from src.models import Question

router = Router()


class AddQuestionState(StatesGroup):
    question = State()
    answer = State()
    accept = State()


class EditQuestionState(StatesGroup):
    question = State()
    answer = State()


@router.callback_query(F.data == 'admin-manage-faq', StateFilter(None))
async def on_faq(callback: types.CallbackQuery):
    await callback.answer('➡️ Переход в ❓ Вопросы FAQ')

    text = 'Вы перешли в <b>❓ FAQ</b> - раздел с часто задаваемыми вопросами\n\n' \
           '<i>↘️ Выберите действие</i>'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='➕ Добавить вопрос',
                                           callback_data='add-question')
            ],
            [
                types.InlineKeyboardButton(text='📒 Перейти к списку',
                                           callback_data='faq-list')
            ]
        ]
    )
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'add-question', StateFilter(None))
async def on_add_faq(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.set_state(AddQuestionState.question)
    text = 'Введите вопрос\n\n' \
           '❕ <i>Вопрос должен быть текстового содержания</i>'
    await callback.message.answer(text)


@router.message(AddQuestionState.question)
async def on_add_faq_question(message: types.Message, state: FSMContext):
    await state.set_state(AddQuestionState.answer)
    await state.update_data({'question': message.text})

    text = 'Введите ответ для вашего вопрос\n\n' \
           '<i>❕ Ответ тоже должен быть текстового содержания</i>'
    await message.answer(text)


@router.message(AddQuestionState.answer)
async def on_add_faq_answer(message: types.Message, state: FSMContext):
    await state.set_state(AddQuestionState.accept)
    await state.update_data({'answer': message.text})

    data = await state.get_data()
    text = '📋 Данные вопроса\n\n' \
           f'<b>Вопрос</b>: {data.get("question")}\n' \
           f'<b>Ответ</b>: {data.get("answer")}\n\n' \
           '<i>↘️ Выберите действие</i>'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='✅ Сохранить', callback_data='save-question'),
                types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')
            ]
        ]
    )

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'save-question', AddQuestionState.accept)
async def on_add_question_accept(callback: types.CallbackQuery, state: FSMContext, db: sessionmaker):
    await callback.answer('')
    await callback.message.edit_reply_markup()

    data = await state.get_data()
    question = data.get('question')
    answer = data.get('answer')

    await Question.new(db, question, answer)

    text = '✅ Вопрос успешно сохранен'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='↖️ Назад в список',
                    callback_data='faq-list'
                )
            ]
        ]
    )
    await callback.message.answer(text, reply_markup=keyboard)

    await state.clear()

    await asyncio.sleep(0.5)


@router.callback_query(F.data == 'faq-list', StateFilter(None))
@router.callback_query(F.data.startswith('faq-action'), StateFilter(None))
async def on_faq_list(callback: types.CallbackQuery, db: sessionmaker):
    await callback.answer()
    await callback.message.edit_reply_markup()

    text = '📄 Список вопросов'

    buttons = await FAQListKeyboard.get_buttons(db, 'faq-question')
    keyboard = FAQListKeyboard(buttons, 'faq-action')

    if callback.data.startswith('faq-action'):
        prefix, index = callback.data.split('_')
        await callback.message.edit_text(text, reply_markup=keyboard.as_keyboard(int(index)))
        return

    await callback.message.answer(text, reply_markup=keyboard.as_keyboard(0))


@router.callback_query(F.data.startswith('faq-question'), StateFilter(None))
async def on_faq_question(callback: types.CallbackQuery, db: sessionmaker):
    await callback.answer()

    prefix, index = callback.data.split('_')
    question_id = int(index)
    question = await Question.get(db, question_id)

    text = f'<b>ID</b>: <code>{question[0].id}</code>\n\n' \
           f'<b>Вопрос</b>: {question[0].question}\n' \
           f'<b>Ответ</b>: {question[0].answer}\n\n' \
           '<i>↘️ Выберите действие</i>'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='✏️ Редактировать',
                                           callback_data=f'edit-faq_{index}'),
                types.InlineKeyboardButton(text='🚫 Удалить',
                                           callback_data=f'delete-faq-question_{index}')
            ],
            [
                types.InlineKeyboardButton(text='↩️ Назад', callback_data='faq-action_0')
            ]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('delete-faq'), StateFilter(None))
async def on_delete_faq(callback: types.CallbackQuery, db):
    await callback.message.edit_reply_markup()
    await callback.answer()

    prefix, index = callback.data.split('_')

    text = f'❎ Вопрос с <b>ID</b> {index} удален'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='↖️ Назад в список', callback_data='faq-list')
            ]
        ]
    )

    await Question.delete(db, int(index))
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('edit-faq'), StateFilter(None))
async def on_edit_faq_question(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()

    prefix, index = callback.data.split('_')

    text = '📝 Редактировать <b>вопрос</b>\n\n' \
           '↘️ <i>Выберите действие</i>'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='✏️ Изменить вопрос',
                                           callback_data=f'edit-question-faq_{index}'),
                types.InlineKeyboardButton(text='✏️ Изменить ответ',
                                           callback_data=f'edit-answer-faq_{index}')
            ],
            [
                types.InlineKeyboardButton(text='⬅️ Назад', callback_data='faq_list')
            ]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('edit-question-faq'), StateFilter(None))
async def on_edit_faq_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await state.set_state(EditQuestionState.question)

    prefix, index = callback.data.split('_')
    await state.update_data({'id': index})

    text = 'Введите новый вопрос\n\n' \
           '❕ <i>Вопрос должен быть текстового содержания</i>'
    await callback.message.answer(text)


@router.message(EditQuestionState.question)
async def on_edit_faq_new_question(message: types.Message, state: FSMContext, db):
    data = await state.get_data()
    _id = data.get('id')

    question = message.text

    await Question.edit_question(db, int(_id), question)

    text = '☑️ Данные вопроса успешно обновлены'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='↖️ Назад в список', callback_data='faq-list')
            ]
        ]
    )
    await message.answer(text, reply_markup=keyboard)

    await state.clear()


@router.callback_query(F.data.startswith('edit-answer-faq'), StateFilter(None))
async def on_edit_faq_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await state.set_state(EditQuestionState.answer)

    prefix, index = callback.data.split('_')
    await state.update_data({'id': index})

    text = 'Введите новый ответ\n\n' \
           '❕ <i>Ответ должен быть текстового содержания</i>'
    await callback.message.answer(text)


@router.message(EditQuestionState.answer)
async def on_edit_faq_new_answer(message: types.Message, state: FSMContext, db):
    data = await state.get_data()
    _id = data.get('id')

    answer = message.text

    await Question.edit_answer(db, int(_id), answer)

    text = '☑️ Данные вопроса успешно обновлены'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='↖️ Назад в список', callback_data='faq-list')
            ]
        ]
    )
    await message.answer(text, reply_markup=keyboard)

    await state.clear()
