from aiogram import Bot, types
from aiogram.filters import BaseFilter
from sqlalchemy.orm import sessionmaker

from models import Operator
from src.config import Config



class AdminFilter(BaseFilter):

    async def __call__(self, get: types.Message | types.CallbackQuery, config: Config):
        return get.from_user.id in config.bot.admin_ids


class UserFilter(AdminFilter):

    async def __call__(self, get: types.Message | types.CallbackQuery, config: Config):
        return not await super().__call__(get, config)


class OperatorFilter(BaseFilter):

    async def __call__(self, get: types.Message | types.CallbackQuery, db: sessionmaker):
        user_id = get.from_user.id
        operator = await Operator.get(db, user_id)
        if operator:
            return True
        return False