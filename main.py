# main.py

"""
Основной модуль для запуска бота.
- Инициализирует бота и диспетчер.
- Регистрирует все хэндлеры (команды, callback-запросы).
- Запускает процесс поллинга для получения обновлений от Telegram.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F

from config import API_TOKEN  # Импорт токена бота из конфигурации
from database.db import create_table  # Импорт функции для создания таблицы в БД
from handlers.start import cmd_start  # Импорт хэндлера для команды /start
from handlers.quiz import (
    cmd_quiz,
)  # Импорт для кнопки "Начать игру"
from handlers.callbacks import (
    register_callbacks,
)  # Импорт функции для регистрации callback-хэндлеров
from handlers.stats import cmd_stats  # Импорт хэндлера для команды /stats

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация хэндлеров
dp.message.register(cmd_start, Command("start"))  # Регистрация команды /start
dp.message.register(
    cmd_quiz, F.text == "Начать игру"
)  # Регистрация кнопки "Начать игру"
dp.message.register(cmd_stats, Command("stats"))  # Регистрация команды /stats

# Регистрация callback-хэндлеров
register_callbacks(dp)


# Основная функция для запуска бота
async def main():
    await create_table()  # Создание таблицы в базе данных (если она не существует)
    await dp.start_polling(bot)  # Запуск бота


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной функции main
