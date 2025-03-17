# database/db.py

"""
Модуль для работы с базой данных.
- Создает таблицу для хранения состояния квиза.
- Управляет текущим индексом вопроса для каждого пользователя.
"""

import aiosqlite
from config import DB_NAME  # Импорт имени базы данных из конфигурации

async def create_table():
    """
    Создает таблицы `quiz_state`, `quiz_statistics` и `quiz_history` в базе данных, если они не существуют.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для хранения текущего состояния квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Таблица для хранения текущей статистики
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_statistics (user_id INTEGER PRIMARY KEY, correct_answers INTEGER, total_questions INTEGER)''')
        # Таблица для хранения истории попыток
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_history (
            user_id INTEGER,
            correct_answers INTEGER,
            total_questions INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        await db.commit()  # Сохраняем изменения

async def get_quiz_index(user_id):
    """
    Получает текущий индекс вопроса для пользователя из базы данных.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()  # Получаем результат запроса
            if results is not None:
                return results[0]  # Возвращаем индекс вопроса
            else:
                return 0  # Если запись не найдена, возвращаем 0

async def update_quiz_index(user_id, index):
    """
    Обновляет текущий индекс вопроса для пользователя в базе данных.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))  # Вставляем или обновляем запись
        await db.commit()  # Сохраняем изменения

async def update_statistics(user_id, is_correct):
    """
    Обновляет статистику ответов пользователя.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем текущую статистику
        async with db.execute('SELECT correct_answers, total_questions FROM quiz_statistics WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()

        if result:
            correct_answers, total_questions = result
            correct_answers += 1 if is_correct else 0
            total_questions += 1
            await db.execute('UPDATE quiz_statistics SET correct_answers = ?, total_questions = ? WHERE user_id = ?', (correct_answers, total_questions, user_id))
        else:
            # Если запись не существует, создаем новую
            correct_answers = 1 if is_correct else 0
            total_questions = 1
            await db.execute('INSERT INTO quiz_statistics (user_id, correct_answers, total_questions) VALUES (?, ?, ?)', (user_id, correct_answers, total_questions))

        await db.commit()

async def get_statistics(user_id):
    """
    Получает статистику ответов пользователя.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers, total_questions FROM quiz_statistics WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result  # Возвращаем (correct_answers, total_questions)
            else:
                return (0, 0)  # Если статистики нет, возвращаем нули
            
async def save_quiz_attempt(user_id, correct_answers, total_questions):
    """
    Сохраняет результат попытки прохождения квиза в таблицу `quiz_history`.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO quiz_history (user_id, correct_answers, total_questions) VALUES (?, ?, ?)', (user_id, correct_answers, total_questions))
        await db.commit()

async def get_quiz_history(user_id):
    """
    Получает историю попыток прохождения квиза для пользователя.
    Возвращает список кортежей (correct_answers, total_questions).
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers, total_questions FROM quiz_history WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchall()
            return results
