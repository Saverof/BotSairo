# config.py

import os

from dotenv import load_dotenv

"""
Модуль для хранения конфигурационных данных.
- Содержит токен бота и имя базы данных.
- Упрощает изменение настроек без необходимости редактирования основного кода.
"""

# Загружаем переменные из .env
load_dotenv()

# Конфигурационные данные для бота
API_TOKEN = os.getenv("API_TOKEN")  # Получаем токен бота
if not API_TOKEN:
    raise ValueError(
        "Токен бота не найден. Убедитесь, что файл .env существует и содержит API_TOKEN."
    )
DB_NAME = "quiz_bot.db"  # Имя файла базы данных SQLite
