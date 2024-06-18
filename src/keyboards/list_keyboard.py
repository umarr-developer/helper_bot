from aiogram import types
from sqlalchemy.orm import sessionmaker

from src.models.questions import Question


class ListKeyboard:
    element_count: int = 4

    def __init__(self, buttons: list[types.InlineKeyboardButton], action_prefix: str):
        self.buttons = buttons
        self.action_prefix = action_prefix

        self.previous_button = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='')
        self.next_button = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='')

    def as_keyboard(self, index: int):
        self.previous_button.callback_data = f'{self.action_prefix}_{index - self.element_count}'
        self.next_button.callback_data = f'{self.action_prefix}_{index + self.element_count}'

        action_buttons = []
        list_buttons = self.buttons[index:index + self.element_count:]

        if index != 0 and len(self.buttons) > index + self.element_count:
            action_buttons.append(self.previous_button)
            action_buttons.append(self.next_button)
        elif index == 0:
            action_buttons.append(self.next_button)
        elif len(self.buttons) <= index + self.element_count:
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
        questions: list[tuple[Question]] = await Question.all(db_session=db)

        return [
            types.InlineKeyboardButton(
                text=f'❓ {question[0].question}',
                callback_data=f'{question_prefix}_{question[0].id}')
            for question in questions
        ]
