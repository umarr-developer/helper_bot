from aiogram import types

from src.models import User


class UserManageSwitchKeyboard:

    def __init__(self, user: User):
        self.user = user
        self.block_buttons = {
            False: types.InlineKeyboardButton(
                text='❎ Заблокировать пользователя', callback_data=f'admin-block-user_{user.user_id}'
            ),
            True: types.InlineKeyboardButton(
                text='✅ Разблокировать пользователя', callback_data=f'admin-unblock-user_{user.user_id}'
            )
        }
        self.call_operator_buttons = {
            True: types.InlineKeyboardButton(
                text='❎ Закрыть доступ к оператору',
                callback_data=f'admin-block-call-operator_{user.user_id}'
            ),
            False: types.InlineKeyboardButton(
                text='✅ Открыть доступ к оператору',
                callback_data=f'admin-unblock-call-operator_{user.user_id}'
            )
        }
        self.send_ticket_buttons = {
            True: types.InlineKeyboardButton(
                text='❎ Закрыть доступ к тикетами',
                callback_data=f'admin-block-send-ticket_{user.user_id}'
            ),
            False: types.InlineKeyboardButton(
                text='✅ Открыть доступ к тикетами',
                callback_data=f'admin-unblock-send-ticket_{user.user_id}'
            )
        }

    def as_keyboard(self):
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [self.block_buttons[self.user.blocked]],
                [self.call_operator_buttons[self.user.call_operator]],
                [self.send_ticket_buttons[self.user.send_ticket]]
            ]
        )
