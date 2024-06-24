from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from src.models import User


class BlockedUserMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler,
                       event: types.Message | types.CallbackQuery,
                       data: dict) -> any:
        user: tuple['User'] = data.get('user')
        if user:
            if user[0].blocked:
                return 
        return await handler(event, data)
