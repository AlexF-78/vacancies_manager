from abc import ABC, abstractmethod

# import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""

    @abstractmethod
    def __init__(self):
        self._base_url = None

    @abstractmethod
    def _connect(self):
        """
        Приватный метод для подключения к API.
        Проверяет, что подключение возможно и возвращает ответ.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int = 100):
        """
        Абстрактный метод для получения вакансий по ключевому слову.
        :param keyword: Ключевое слово для поиска
        :param per_page: Количество вакансий на странице (по умолчанию 100)
        """
        pass
