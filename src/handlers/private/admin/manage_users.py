from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from src.keyboards import UserManageSwitchKeyboard
from src.models import User

router = Router()


class SearchUserState(StatesGroup):
    search = State()


@router.callback_query(F.data == 'admin-manage-users', StateFilter(None))
async def on_manage_users(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SearchUserState.search)

    text = 'Отправьте <b>ID</b> пользователя или же переотправьте его сообщение в этот чат'
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')
            ]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard)


@router.message(SearchUserState.search)
async def on_manage_users_search(message: types.Message, db: sessionmaker, state: FSMContext, bot: Bot):
    if message.forward_from:
        user_id = message.forward_from.id
    elif message.text.isdigit():
        user_id = int(message.text)
    else:
        text = '🚫 Некорректиные данные. <i>Повторите еще раз</i>'
        await message.answer(text)
        return

    user = await User.get(db, user_id)
    chat = await bot.get_chat(user_id)

    if not user:
        text = '🚫 Пользователь не найден'
        await message.answer(text)
        return

    text = f'Найден пользователь c <b>ID {user[0].id}</b>\n\n' \
           f'<b>USER ID</b>: <code>{user[0].user_id}</code>\n' \
           f'<b>ФИО</b>: <code>{chat.full_name}</code>\n' \
           f'<b>Дата запуска бота</b>: <code>{user[0].created_on}</code>\n\n' \
           '↘️ Выберите действие с пользоватлем'
    keyboard = UserManageSwitchKeyboard(user[0])
    await message.answer(text, reply_markup=keyboard.as_keyboard())

    await state.clear()


@router.callback_query(F.data.startswith('admin-block-user'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.block(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-unblock-user'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.unblock(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-block-call-operator'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.block_call_operator(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-unblock-call-operator'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.unblock_call_operator(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-block-send-ticket'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.block_send_ticket(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())


@router.callback_query(F.data.startswith('admin-unblock-send-ticket'))
async def on_manage_user_block_user(callback: types.CallbackQuery, db: sessionmaker):
    prefix, user_id = callback.data.split('_')
    user_id = int(user_id)

    await User.unblock_send_ticket(db, user_id)

    user = await User.get(db, user_id)
    keyboard = UserManageSwitchKeyboard(user[0])
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_keyboard())
