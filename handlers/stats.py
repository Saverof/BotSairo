# handlers/stats.py

from aiogram import types
from database.db import get_quiz_history


async def cmd_stats(message: types.Message):
    """
    Обрабатывает команду /stats.
    - Выводит количество попыток.
    - Лучший результат.
    - Процентную долю правильных ответов за все попытки.
    """
    user_id = message.from_user.id
    history = await get_quiz_history(user_id)  # Получаем историю попыток

    if not history:
        await message.answer("⏳ Вы еще не проходили квиз.")
        return

    # Количество попыток
    total_attempts = len(history)

    # Лучший результат
    best_result = max(
        history, key=lambda x: x[0]
    )  # Максимальное количество правильных ответов
    best_score = f"{best_result[0]}/{best_result[1]}"

    # Общее количество правильных ответов и вопросов
    total_correct = sum(attempt[0] for attempt in history)
    total_questions = sum(attempt[1] for attempt in history)

    # Процентная доля правильных ответов
    if total_questions > 0:
        success_rate = (total_correct / total_questions) * 100
    else:
        success_rate = 0

    # Формируем сообщение
    stats_message = (
        f"📊 Ваша статистика:\n"
        f"• 🎯 Количество попыток: {total_attempts}\n"
        f"• 🏆 Лучший результат: {best_score}\n"
        f"• 📈 Процент правильных ответов: {success_rate:.2f}%"
    )
    await message.answer(stats_message)
