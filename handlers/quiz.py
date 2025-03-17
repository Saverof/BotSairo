# handlers/quiz.py

"""
Модуль для обработки квиза.
- Управляет вопросами и ответами.
- Отправляет вопросы пользователю и обрабатывает их ответы.
- Взаимодействует с базой данных для хранения текущего состояния квиза.
"""

from aiogram import types
import aiosqlite

from config import DB_NAME
from database.db import (
    update_quiz_index,
    get_quiz_index,
)  # Импорт функций для работы с базой данных
from utils.quiz_data import quiz_data  # Импорт данных для квиза
from keyboards.inline import (
    generate_options_keyboard,
)  # Импорт функции для создания inline-клавиатуры


async def get_question(message, user_id):
    """
    Получает текущий вопрос для пользователя и отправляет его с вариантами ответов.
    - Добавляет номер вопроса и значок 📝 перед текстом вопроса.
    """
    current_question_index = await get_quiz_index(
        user_id
    )  # Получаем текущий индекс вопроса
    question_data = quiz_data[
        current_question_index
    ]  # Получаем данные текущего вопроса
    opts = question_data["options"]  # Получаем варианты ответов
    kb = generate_options_keyboard(opts)  # Создаем inline-клавиатуру

    # Формируем текст вопроса с номером и значком 📝
    question_text = f"📝 {current_question_index + 1}. {question_data['question']}"

    await message.answer(
        question_text, reply_markup=kb
    )  # Отправляем вопрос с клавиатурой


async def new_quiz(message):
    """
    Начинает новый квиз для пользователя. Сбрасывает индекс вопроса и статистику.
    """
    user_id = message.from_user.id  # Получаем ID пользователя
    current_question_index = 0  # Сбрасываем индекс вопроса
    await update_quiz_index(
        user_id, current_question_index
    )  # Обновляем индекс вопроса в БД

    # Сбрасываем статистику
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM quiz_statistics WHERE user_id = ?", (user_id,))
        await db.commit()

    await get_question(message, user_id)  # Отправляем первый вопрос


async def cmd_quiz(message: types.Message):
    """
    Обрабатывает кнопку "Начать игру". Запускает новый квиз.
    """
    await message.answer(f"🥁 Давайте начнем!")  # Отправляем сообщение о начале квиза
    await new_quiz(message)  # Запускаем новый квиз
