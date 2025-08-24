import unittest
from unittest.mock import MagicMock, patch

from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    def setUp(self):
        """Подготовка тестового окружения"""
        self.api = HeadHunterAPI()

    @patch('src.hh_api.requests.get')
    def test_connect_success(self, mock_get):
        """Тест успешного подключения к API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.api._connect()
        self.assertEqual(response.status_code, 200)

    @patch('src.hh_api.requests.get')
    def test_connect_failure(self, mock_get):
        """Тест ошибки подключения к API"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.api._connect()

    @patch('src.hh_api.requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        # Мокируем оба вызова requests.get
        mock_connect_response = MagicMock()
        mock_connect_response.status_code = 200

        mock_vacancies_response = MagicMock()
        mock_vacancies_response.status_code = 200
        mock_vacancies_response.json.return_value = {
            'items': [{'id': 1, 'name': 'Python developer'}]
        }

        mock_get.side_effect = [mock_connect_response, mock_vacancies_response]

        vacancies = self.api.get_vacancies('Python')

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Python developer')

    @patch('src.hh_api.requests.get')
    def test_get_vacancies_connection_error(self, mock_get):
        """Тест ошибки при проверке подключения"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.api.get_vacancies('Python')
