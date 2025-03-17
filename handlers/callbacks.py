# handlers/callbacks.py

"""
Модуль для обработки callback-запросов.
- Обрабатывает ответы пользователя на вопросы квиза.
- Определяет, правильный или неправильный ответ был выбран.
- Обновляет статистику ответов.
- Переходит к следующему вопросу или завершает квиз.
- Сохраняет попытки прохождения квиза в историю.
"""

from aiogram import types
from aiogram import F

from database.db import (
    update_quiz_index,
    get_quiz_index,
    update_statistics,
    get_statistics,
    save_quiz_attempt,
)  # Импорт функций для работы с базой данных
from utils.quiz_data import quiz_data  # Импорт данных для квиза
from handlers.quiz import get_question  # Импорт функции для получения вопроса


def register_callbacks(dp):
    """
    Регистрирует callback-хэндлеры для обработки ответов пользователя.
    """

    @dp.callback_query(
        F.data.in_({"0", "1", "2", "3"})
    )  # Обрабатываем только допустимые индексы
    async def handle_answer(callback: types.CallbackQuery):
        """
        Обрабатывает ответ пользователя.
        - Убирает inline-клавиатуру.
        - Отправляет сообщение с результатом ответа.
        - Обновляет статистику.
        - Переходит к следующему вопросу или завершает квиз.
        - Сохраняет попытку в историю, если квиз завершен.
        """
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None,
        )  # Убираем inline-клавиатуру

        current_question_index = await get_quiz_index(
            callback.from_user.id
        )  # Получаем текущий индекс вопроса
        question_data = quiz_data[
            current_question_index
        ]  # Получаем данные текущего вопроса

        # Получаем текст ответа пользователя по индексу
        user_answer_index = int(callback.data)  # Преобразуем callback_data в индекс
        user_answer = question_data["options"][
            user_answer_index
        ]  # Получаем текст ответа

        # Проверяем, правильный ли ответ
        is_correct = user_answer_index == question_data["correct_option"]

        # Отправляем результат ответа
        if is_correct:
            await callback.message.answer(f"✅ Ваш ответ: {user_answer}")
        else:
            await callback.message.answer(f"❌ Ваш ответ: {user_answer}")

        current_question_index += 1  # Увеличиваем индекс вопроса
        await update_quiz_index(
            callback.from_user.id, current_question_index
        )  # Обновляем индекс в БД

        # Обновляем статистику
        await update_statistics(callback.from_user.id, is_correct=is_correct)

        if current_question_index < len(quiz_data):  # Если вопросы не закончились
            await get_question(
                callback.message, callback.from_user.id
            )  # Отправляем следующий вопрос
        else:
            # Получаем статистику
            correct_answers, total_questions = await get_statistics(
                callback.from_user.id
            )
            await callback.message.answer(
                f"Опрос закончен! Ваш результат: {correct_answers}/{total_questions}!"
            )  # Завершаем квиз
            await save_quiz_attempt(
                callback.from_user.id, correct_answers, total_questions
            )  # Сохраняем попытку в историю
