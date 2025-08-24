# Vacancies Manager

Приложение для поиска, сохранения и управления вакансиями с платформы HeadHunter.

##  Возможности

- Поиск вакансий на HeadHunter по ключевым словам
- Сохранение вакансий в JSON-файл
- Просмотр сохраненных вакансий
- Удаление отдельных вакансий по URL
- Очистка всех сохраненных вакансий
- Сравнение вакансий по уровню зарплаты

## Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd vacancies_manager
Создайте виртуальное окружение:

bash
python -m venv venv
Активируйте виртуальное окружение:

Windows:

bash
venv\Scripts\activate
Linux/MacOS:

bash
source venv/bin/activate
Установите зависимости:

bash
pip install -r requirements.txt
Структура проекта
text
vacancies_manager/
├── src/
│   ├── abstract_api.py          # Абстрактный класс API
│   ├── abstract_file_manager.py # Абстрактный класс работы с файлами
│   ├── hh_api.py               # API HeadHunter
│   ├── json_file_manager.py    # Менеджер JSON файлов
│   ├── user_interface.py       # Пользовательский интерфейс
│   ├── utils.py               # Вспомогательные функции
│   ├── vacancy.py             # Модель вакансии
│   └── vacancy_converter.py   # Конвертер вакансий
├── tests/                     # Тесты
├── vacancies.json            # Файл с сохраненными вакансиями
└── main.py                   # Точка входа

---

## Использование
Запустите приложение:

bash
python main.py
Главное меню:
Поиск вакансий - поиск на HH.ru по ключевому слову

Показать сохраненные вакансии - просмотр ранее сохраненных вакансий

Удалить вакансию - удаление вакансии по URL

Очистить все вакансии - полная очистка базы вакансий

Выход - завершение работы приложения

---

## Тестирование
Запуск всех тестов:

bash
python -m unittest discover tests
Запуск конкретного теста:

bash
python -m unittest tests/test_vacancy.py
Проверка стиля кода:

bash
flake8 src/

## Формат данных
Вакансии сохраняются в JSON формате:

json
[
  {
    "title": "Python Developer",
    "url": "https://hh.ru/vacancy/12345",
    "salary_from": 100000,
    "salary_to": 150000,
    "currency": "RUR",
    "requirements": "Опыт работы от 3 лет..."
  }
]
## Технологии
Python 3.8+ - основной язык программирования

requests - HTTP-запросы к API HeadHunter

unittest - модульное тестирование

flake8 - проверка стиля кода

---

## Требования
Python 3.8 или выше

Доступ к интернету (для работы с API HeadHunter)

Установленный pip

---

## Настройка
Приложение использует стандартные настройки:

Файл вакансий: vacancies.json

Количество вакансий на странице: 100

Регион поиска: Россия (код 113)
