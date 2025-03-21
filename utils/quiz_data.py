# utils/quiz_data.py

"""
Модуль для хранения данных квиза.
- Содержит список вопросов, варианты ответов и правильные ответы.
- Упрощает добавление новых вопросов и изменение существующих.
"""

quiz_data = [
    {
        "question": 'Почему язык назвали "Python"?',
        "options": [
            "В честь змеи 🐍",
            'В честь британского комедийного шоу "Monty Python" 🎭',
            "Потому что создатель любил питон-суп 🍲",
            'Это аббревиатура от "Program Your Things Online Now"',
        ],
        "correct_option": 1,
    },
    {
        "question": "Какой тип данных в Python используется для хранения неизменяемых последовательностей?",
        "options": [
            "Список (list)",
            "Кортеж (tuple)",
            "Словарь (dict)",
            "Множество (set)",
        ],
        "correct_option": 1,
    },
    {
        "question": "Что выведет этот код: `print(0.1 + 0.2 == 0.3)`?",
        "options": ["True", "False", "Ошибку", "Ничего, программа зависнет"],
        "correct_option": 1,
    },
    {
        "question": "Какой из этих модулей в Python используется для генерации случайных чисел?",
        "options": ["`math`", "`random`", "`os`", "`datetime`"],
        "correct_option": 1,
    },
    {
        "question": 'Что такое "Zen of Python"?',
        "options": [
            "Философский текст о жизни",
            "Сборник принципов написания красивого кода на Python",
            "Название книги о Python",
            "Секретная команда для запуска Python",
        ],
        "correct_option": 1,
    },
    {
        "question": "Какой из этих операторов используется для возведения в степень в Python?",
        "options": ["`^`", "`**`", "`//`", "`%%`"],
        "correct_option": 1,
    },
    {
        "question": "Что делает функция `len()` в Python?",
        "options": [
            "Возвращает длину строки или коллекции",
            "Увеличивает число на 1",
            "Преобразует строку в число",
            "Ничего, это просто шутка",
        ],
        "correct_option": 0,
    },
    {
        "question": "Какой из этих типов данных в Python является изменяемым?",
        "options": ["Строка (str)", "Кортеж (tuple)", "Список (list)", "Число (int)"],
        "correct_option": 2,
    },
    {
        "question": 'Что выведет этот код: `print("Hello" * 3)`?',
        "options": ["HelloHelloHello", "Hello 3", "Ошибку", "Ничего, это бессмысленно"],
        "correct_option": 0,
    },
    {
        "question": "Какой из этих модулей используется для работы с датой и временем в Python?",
        "options": ["`time`", "`calendar`", "`datetime`", "Все вышеперечисленные"],
        "correct_option": 3,
    },
]
