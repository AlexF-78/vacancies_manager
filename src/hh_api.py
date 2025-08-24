import requests

from abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        # Делаем атрибуты приватными
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'text': '', 'page': 0, 'per_page': 100}

    def _connect(self):
        """
        Приватный метод для подключения к API HH.ru.
        Отправляет запрос на базовый URL и проверяет статус ответа.
        Вызывается перед каждым запросом на получение данных.
        """
        response = requests.get(self._base_url, headers=self._headers, params={})
        # Проверяем, что API доступно и возвращает корректный ответ
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения к HH API! Статус: {response.status_code}")
        return response

    def get_vacancies(self, keyword: str, per_page: int = 100):
        """
        Публичный метод для получения вакансий с HH.ru по ключевому слову.
        :param keyword: Ключевое слово для поиска (например, 'Python developer')
        :param per_page: Количество вакансий для возврата (макс. 100 на страницу для HH)
        :return: Список словарей с вакансиями.
        """
        # 1. Вызываем приватный метод для проверки подключения
        self._connect()

        # 2. Формируем параметры запроса, как минимум 'text' и 'per_page'
        self._params = {
            'text': f'NAME:{keyword}',  # Ищем в названии вакансии
            'area': 113,  # 113 - Россия
            'page': 0,  # Страница
            'per_page': per_page  # Вакансий на страницу
        }

        # 3. Отправляем запрос с нужными параметрами
        response = requests.get(self._base_url, headers=self._headers, params=self._params)
        response.raise_for_status()  # Выбросит исключение, если статус код не 200

        # 4. Преобразуем ответ в JSON и возвращаем список вакансий (items)
        data = response.json()
        vacancies = data['items']

        return vacancies
