from aiogram import types

from src.models import User


class UserManageSwitchKeyboard:

    def __init__(self, user: User):
        self.user = user
        self.block_buttons = {
            False: types.InlineKeyboardButton(
                text='Заблокировать', callback_data=f'admin-block-user_{user.user_id}'
            ),
            True: types.InlineKeyboardButton(
                text='Разблокировать', callback_data=f'admin-unblock-user_{user.user_id}'
            )
        }

    def as_keyboard(self):
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [self.block_buttons[self.user.blocked]]
            ]
        )
