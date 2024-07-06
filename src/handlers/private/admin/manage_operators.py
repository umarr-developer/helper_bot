from aiogram import F, types, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from src.keyboards.list_keyboard import OperatorsListKeyboard
from src.models import User, Operator

router = Router()


class AddOperatorState(StatesGroup):
    search = State()
    username = State()


@router.callback_query(F.data == 'admin-manage-operators', StateFilter(None))
async def on_manage_operators(callback: types.CallbackQuery):
    text = 'Выберите действия'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Добавить оператора',
                                           callback_data='add-operator')
            ],
            [
                types.InlineKeyboardButton(text='Список операторов',
                                           callback_data='operator-list')
            ]
        ]
    )
    await callback.answer()
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'add-operator')
async def on_manage_operators_add_operator(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    text = 'Введите <b>ID</b> оператора. 👨‍💼 <b>Оператор</b> должен быть а базе данных пользователей!'
    await callback.message.answer(text)

    await state.set_state('add_operator')


@router.message(StateFilter('add-operator'))
async def on_manage_operators_add_operator_search(message: types.Message,
                                                  db: sessionmaker,
                                                  state: FSMContext,
                                                  bot: Bot):
    if not message.text.isdigit():
        text = '🚫 Некорректные данные. Попробуйте еще раз'
        await message.answer(text)
        return

    user = await User.get(db, int(message.text))

    if not user:
        text = '🚫 Пользователь не найден. Попробуйте еще раз'
        await message.answer(text)
        return

    operator = await Operator.get(db, int(message.text))
    if not operator:
        chat = await bot.get_chat(message.from_user.id)
        text = f'Найден пользователь c <b>ID {user[0].id}</b>\n\n' \
               f'<b>USER ID</b>: <code>{user[0].user_id}</code>\n' \
               f'<b>ФИО</b>: <code>{chat.full_name}</code>\n' \
               f'<b>Дата регистрации в боте</b>: <code>{user[0].created_on}</code>\n\n'
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Сделать оператором',
                                               callback_data=f'set-operator_{user[0].user_id}')
                ]
            ]
        )

        await message.answer(text, reply_markup=keyboard)
    else:
        text = '❗️ Этот пользователь уже оператор'
        await message.answer(text)

    await state.clear()


@router.callback_query(F.data.startswith('set-operator'))
async def on_manage_operators_set_operator(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    await Operator.new(db, int(user_id))

    text = '✅ Оператор добавлен'
    await callback.message.answer(text)


@router.callback_query(F.data == 'operator-list')
@router.callback_query(F.data.startswith('list-operators-action'))
async def on_manage_operator_list(callback: types.CallbackQuery, db: sessionmaker, bot: Bot):
    buttons = await OperatorsListKeyboard.get_buttons(db, 'list-operators', bot)
    text = '📘 Лист операторов'
    keyboard = OperatorsListKeyboard(buttons, 'list-operators-action')

    if callback.data.startswith('list-operators-action'):
        prefix, index = callback.data.split('_')
        await callback.message.edit_text(text, reply_markup=keyboard.as_keyboard(int(index)))
        return

    await callback.message.answer(text, reply_markup=keyboard.as_keyboard(0))
