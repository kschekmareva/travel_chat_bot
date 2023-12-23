from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_factories.edit_items import RegionsCallbackFactory, CityCallbackFactory, CountryCallbackFactory, \
    CharCallbackFactory


def create_keyboard(*args: str, callback_factory) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=button[1],
                callback_data=callback_factory(id=button[0], item=button[1]).pack()
            )
        )
    return kb_builder.as_markup()


def create_char_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками
    for char in sorted(args):
        kb_builder.add(
            InlineKeyboardButton(
                text=char,
                callback_data=CharCallbackFactory(char=char).pack()
            )
        )
    return kb_builder.as_markup()
