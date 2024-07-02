from aiogram import types, Bot
from sqlalchemy.orm import sessionmaker

from src.models import Operator
from src.models.questions import Question


class ListKeyboard:
    element_count: int = 4

    def __init__(self, buttons: list[types.InlineKeyboardButton], action_prefix: str):
        self.buttons = buttons
        self.action_prefix = action_prefix

        self.previous_button = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='')
        self.next_button = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='')

    def as_keyboard(self, index: int = 0):
        self.previous_button.callback_data = f'{self.action_prefix}_{index - self.element_count}'
        self.next_button.callback_data = f'{self.action_prefix}_{index + self.element_count}'

        action_buttons = []
        list_buttons = self.buttons[index:index + self.element_count:]

        if index != 0 and len(self.buttons) > index + self.element_count:
            action_buttons.append(self.previous_button)
            action_buttons.append(self.next_button)
        elif index == 0 and len(self.buttons) > index + self.element_count:
            action_buttons.append(self.next_button)
        elif len(self.buttons) <= index + self.element_count and index != 0:
            action_buttons.append(self.previous_button)

        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                *[[button] for button in list_buttons],
                action_buttons
            ]
        )


class FAQListKeyboard(ListKeyboard):
    element_count: int = 6

    @staticmethod
    async def get_buttons(db: sessionmaker, question_prefix) -> list[types.InlineKeyboardButton]:
        inline_buttons = []
        questions: list[tuple[Question]] = await Question.all(db_session=db)

        for question in questions:
            inline_buttons.append(
                types.InlineKeyboardButton(
                    text=f'❓ {question[0].question}',
                    callback_data=f'{question_prefix}_{question[0].id}'
                )
            )

        return inline_buttons


class OperatorsListKeyboard(ListKeyboard):
    element_count: int = 8

    @staticmethod
    async def get_buttons(db: sessionmaker, prefix: str, bot: Bot) -> list[types.InlineKeyboardButton]:
        operators: list[tuple[Operator]] = await Operator.all(db_session=db)
        inline_buttons = []

        for operator in operators:
            user = await bot.get_chat(operator[0].user_id)

            inline_buttons.append(
                types.InlineKeyboardButton(
                    text=user.full_name,
                    callback_data=f'{prefix}_{operator[0].user_id}'
                )
            )

        return inline_buttons
