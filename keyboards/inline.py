# keyboards/inline.py

"""
Модуль для создания inline-клавиатур.
- Генерирует клавиатуру с вариантами ответов для вопросов квиза.
- Определяет, какой ответ правильный, и присваивает соответствующий callback_data.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def generate_options_keyboard(answer_options):
    """
    Создает inline-клавиатуру с вариантами ответов.
    - Передает индекс ответа в callback_data.
    """
    builder = InlineKeyboardBuilder()
    for index, option in enumerate(
        answer_options
    ):  # Используем enumerate для получения индекса
        builder.add(
            types.InlineKeyboardButton(
                text=option,
                callback_data=str(index),  # Передаем индекс ответа в callback_data
            )
        )  # Добавляем кнопку с вариантом ответа
    builder.adjust(1)  # Настраиваем клавиатуру (одна кнопка в строке)
    return builder.as_markup()  # Возвращаем готовую клавиатуру
