from typing import Any, Dict, List

from abstract_file_manager import AbstractFileManager
from utils import (create_backup_file, filter_data_by_criteria,
                   filter_duplicates_by_url, load_json_data, save_json_data,
                   validate_file_exists)


class JSONFileManager(AbstractFileManager):
    """
    Класс для работы с JSON-файлами.
    Наследуется от AbstractFileManager.
    Использует вспомогательные функции из модуля utils.
    """

    def __init__(self, filename: str = "vacancies.json"):
        """
        Инициализация менеджера JSON-файлов.
        :param filename: Имя файла (по умолчанию 'vacancies.json')
        """
        self._filename = filename
        validate_file_exists(filename)

    def get_data(self) -> List[Dict[str, Any]]:
        """
        Получение данных из JSON-файла.
        :return: Список словарей с данными вакансий
        """
        return load_json_data(self._filename)

    def add_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Добавление данных в JSON-файл без дубликатов.
        :param data: Список словарей с данными вакансий
        """
        if not data:
            return

        existing_data = self.get_data()
        filtered_data = filter_duplicates_by_url(data, existing_data)

        if filtered_data:
            updated_data = existing_data + filtered_data
            save_json_data(self._filename, updated_data)

    def delete_data(self, criteria: Dict[str, Any]) -> None:
        """
        Удаление данных из файла по критериям.
        :param criteria: Словарь с критериями удаления
        """
        # Создаем резервную копию перед удалением
        backup_path = create_backup_file(self._filename)
        if backup_path:
            print(f"Создана резервная копия: {backup_path}")

        existing_data = self.get_data()
        filtered_data = filter_data_by_criteria(existing_data, criteria)
        save_json_data(self._filename, filtered_data)

    def clear_all_data(self) -> None:
        """Очистка всех данных из файла."""
        save_json_data(self._filename, [])
