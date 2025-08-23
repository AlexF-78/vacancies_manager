import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


def validate_file_exists(filename: str) -> None:
    """
    Проверяет существование файла и создает его, если необходимо.

    :param filename: Путь к файлу для проверки
    :type filename: str
    :raises OSError: Если невозможно создать файл
    """
    if not os.path.exists(filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if filename.endswith('.json'):
                    json.dump([], file)
                elif filename.endswith('.txt'):
                    file.write('')
        except OSError as e:
            raise OSError(f"Не удалось создать файл {filename}: {e}")


def filter_duplicates_by_url(
        new_data: List[Dict[str, Any]],
        existing_data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Фильтрует дубликаты вакансий по URL из новых данных.

    :param new_data: Список новых данных для фильтрации
    :type new_data: List[Dict[str, Any]]
    :param existing_data: Список существующих данных для сравнения
    :type existing_data: List[Dict[str, Any]]
    :return: Отфильтрованный список данных без дубликатов
    :rtype: List[Dict[str, Any]]
    """
    if not existing_data:
        return new_data

    existing_urls = {item.get('url', '') for item in existing_data if item.get('url')}

    return [
        item for item in new_data
        if item.get('url') and item['url'] not in existing_urls
    ]


def load_json_data(filename: str) -> List[Dict[str, Any]]:
    """
    Загружает данные из JSON файла.

    :param filename: Путь к JSON файлу
    :type filename: str
    :return: Список данных из файла
    :rtype: List[Dict[str, Any]]
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json_data(filename: str, data: List[Dict[str, Any]]) -> None:
    """
    Сохраняет данные в JSON файл с форматированием.

    :param filename: Путь к JSON файлу
    :type filename: str
    :param data: Данные для сохранения
    :type data: List[Dict[str, Any]]
    :raises IOError: Если не удалось записать в файл
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except IOError as e:
        raise IOError(f"Не удалось записать в файл {filename}: {e}")


def filter_data_by_criteria(
        data: List[Dict[str, Any]],
        criteria: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Фильтрует данные по заданным критериям.

    :param data: Данные для фильтрации
    :type data: List[Dict[str, Any]]
    :param criteria: Критерии фильтрации (ключ-значение)
    :type criteria: Dict[str, Any]
    :return: Отфильтрованные данные
    :rtype: List[Dict[str, Any]]
    """
    if not criteria:
        return data

    return [
        item for item in data
        if not all(item.get(key) == value for key, value in criteria.items())
    ]


def convert_vacancy_to_dict(vacancy: Any) -> Dict[str, Any]:
    """
    Конвертирует объект вакансии в словарь.

    :param vacancy: Объект вакансии
    :type vacancy: Any (ожидается объект с атрибутами title, url и т.д.)
    :return: Словарь с данными вакансии
    :rtype: Dict[str, Any]
    """
    return {
        'title': getattr(vacancy, 'title', ''),
        'url': getattr(vacancy, 'url', ''),
        'salary_from': getattr(vacancy, 'salary_from', 0),
        'salary_to': getattr(vacancy, 'salary_to', 0),
        'currency': getattr(vacancy, 'currency', ''),
        'requirements': getattr(vacancy, 'requirements', ''),
        'date_created': datetime.now().isoformat()
    }


def convert_dict_to_vacancy(data: Dict[str, Any], vacancy_class: Any) -> Any:
    """
    Конвертирует словарь в объект вакансии.

    :param data: Словарь с данными вакансии
    :type data: Dict[str, Any]
    :param vacancy_class: Класс для создания объекта вакансии
    :type vacancy_class: Any
    :return: Объект вакансии
    :rtype: Any
    """
    return vacancy_class(
        title=data.get('title', ''),
        url=data.get('url', ''),
        salary_from=data.get('salary_from', 0),
        salary_to=data.get('salary_to', 0),
        currency=data.get('currency', ''),
        requirements=data.get('requirements', '')
    )


def validate_salary_values(salary_from: Optional[int], salary_to: Optional[int]) -> tuple[int, int]:
    """
    Валидирует и нормализует значения зарплаты.

    :param salary_from: Нижняя граница зарплаты
    :type salary_from: Optional[int]
    :param salary_to: Верхняя граница зарплаты
    :type salary_to: Optional[int]
    :return: Кортеж с нормализованными значениями (from, to)
    :rtype: tuple[int, int]
    """
    validated_from = salary_from if isinstance(salary_from, int) and salary_from >= 0 else 0
    validated_to = salary_to if isinstance(salary_to, int) and salary_to >= 0 else 0

    # Если указаны обе границы, проверяем что from <= to
    if validated_from and validated_to and validated_from > validated_to:
        validated_from, validated_to = validated_to, validated_from

    return validated_from, validated_to


def format_salary_string(salary_from: int, salary_to: int, currency: str) -> str:
    """
    Форматирует строку с информацией о зарплате.

    :param salary_from: Нижняя граница зарплаты
    :type salary_from: int
    :param salary_to: Верхняя граница зарплаты
    :type salary_to: int
    :param currency: Валюта зарплаты
    :type currency: str
    :return: Отформатированная строка зарплаты
    :rtype: str
    """
    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} {currency}"
    elif salary_from:
        return f"от {salary_from} {currency}"
    elif salary_to:
        return f"до {salary_to} {currency}"
    else:
        return "не указана"


def get_user_input(prompt: str, validation_func: Optional[callable] = None) -> str:
    """
    Получает ввод от пользователя с валидацией.

    :param prompt: Подсказка для пользователя
    :type prompt: str
    :param validation_func: Функция для валидации ввода (опционально)
    :type validation_func: Optional[callable]
    :return: Введенные пользователем данные
    :rtype: str
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Поле не может быть пустым. Попробуйте снова.")
            continue

        if validation_func and not validation_func(user_input):
            print("Некорректный ввод. Попробуйте снова.")
            continue

        return user_input


def display_vacancies_list(vacancies: List[Any], limit: int = 10) -> None:
    """
    Выводит список вакансий в удобочитаемом формате.

    :param vacancies: Список вакансий для отображения
    :type vacancies: List[Any]
    :param limit: Максимальное количество вакансий для отображения
    :type limit: int
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"\nНайдено вакансий: {len(vacancies)}")
    print("-" * 80)

    for i, vacancy in enumerate(vacancies[:limit], 1):
        salary_str = format_salary_string(
            getattr(vacancy, 'salary_from', 0),
            getattr(vacancy, 'salary_to', 0),
            getattr(vacancy, 'currency', '')
        )

        print(f"{i}. {getattr(vacancy, 'title', 'Без названия')}")
        print(f"   Зарплата: {salary_str}")
        print(f"   Ссылка: {getattr(vacancy, 'url', 'Не указана')}")
        print(f"   Требования: {getattr(vacancy, 'requirements', 'Не указаны')[:100]}...")
        print("-" * 80)

    if len(vacancies) > limit:
        print(f"... и еще {len(vacancies) - limit} вакансий")


def create_backup_file(original_filename: str) -> str:
    """
    Создает резервную копию файла.

    :param original_filename: Путь к оригинальному файлу
    :type original_filename: str
    :return: Путь к созданной резервной копии
    :rtype: str
    """
    if not os.path.exists(original_filename):
        return ""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{original_filename}.backup_{timestamp}"

    try:
        with open(original_filename, 'r', encoding='utf-8') as src:
            with open(backup_filename, 'w', encoding='utf-8') as dst:
                if original_filename.endswith('.json'):
                    json.dump(json.load(src), dst, ensure_ascii=False, indent=2)
                else:
                    dst.write(src.read())
        return backup_filename
    except Exception as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return ""


def format_number(number: int) -> str:
    """
    Форматирует число с разделителями тысяч.

    :param number: Число для форматирования
    :type number: int
    :return: Отформатированная строка числа
    :rtype: str
    """
    return f"{number:,}".replace(",", " ")


def confirm_action(prompt: str) -> bool:
    """
    Запрашивает подтверждение действия у пользователя.

    :param prompt: Вопрос для подтверждения
    :type prompt: str
    :return: True если пользователь подтвердил, иначе False
    :rtype: bool
    """
    response = get_user_input(f"{prompt} (да/нет): ",
                              lambda x: x.lower() in ['да', 'нет', 'д', 'н', 'yes', 'no', 'y', 'n'])
    return response.lower() in ['да', 'д', 'yes', 'y']
