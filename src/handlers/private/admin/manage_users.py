from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from src.keyboards.switch_keyboard import UserManageSwitchKeyboard
from src.models import User

router = Router()


class SearchUserState(StatesGroup):
    search = State()


@router.callback_query(F.data == 'admin_manage_users', StateFilter(None))
async def on_manage_users(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SearchUserState.search)

    text = 'Отправьте <b>ID</b> пользователя или же переотправьте его сообщение в этот чат'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Отмена', callback_data='admin_cancel')
            ]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard)


@router.message(SearchUserState.search)
async def on_manage_users_search(message: types.Message, db: sessionmaker, state: FSMContext):
    if message.forward_from:
        user_id = message.forward_from.id
    elif message.text.isdigit():
        user_id = int(message.text)
    else:
        text = 'Некорректиные данные. Повторите еще раз'
        await message.answer(text)
        return

    user = await User.get(db, user_id)

    if not user:
        text = 'Пользователь не найден'
        await message.answer(text)
        return

    text = f'Найден пользователь с ID {user[0].id}'
    keyboard = UserManageSwitchKeyboard(user[0])
    await message.answer(text, reply_markup=keyboard.as_keyboard())
    await state.clear()


@router.callback_query(F.data.startswith('admin-block-user'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    print(callback.data)
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.block(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-unblock-user'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    print(callback.data)
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.unblock(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())
