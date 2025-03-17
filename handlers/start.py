# handlers/start.py

"""
Модуль для обработки команды /start.
- Отправляет приветственное сообщение.
- Предлагает пользователю начать игру с помощью кнопки "Начать игру".
"""

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Хэндлер для команды /start
async def cmd_start(message: types.Message):
    """
    Обрабатывает команду /start. Отправляет приветственное сообщение и кнопку "Начать игру".
    """
    builder = ReplyKeyboardBuilder()  # Создаем билдер для клавиатуры
    builder.add(
        types.KeyboardButton(text="Начать игру")
    )  # Добавляем кнопку "Начать игру"
    await message.answer(
        "👋🏻 Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )  # Отправляем сообщение с клавиатурой
