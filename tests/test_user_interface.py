import unittest
from unittest.mock import MagicMock, patch

from src.user_interface import UserInterface


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        """Подготовка тестового окружения"""
        self.ui = UserInterface()
        # Мокаем экземпляры, которые создаются в __init__
        self.ui.hh_api = MagicMock()
        self.ui.file_manager = MagicMock()

    @patch('src.user_interface.get_user_input')
    def test_get_menu_choice(self, mock_input):
        """Тест получения выбора из меню"""
        mock_input.return_value = '1'
        result = self.ui._get_menu_choice()
        self.assertEqual(result, '1')
        mock_input.assert_called_once()

    @patch('src.user_interface.VacancyFactory')
    @patch('src.user_interface.get_user_input')
    @patch('src.user_interface.display_vacancies_list')
    def test_search_vacancies_success(self, mock_display, mock_input, mock_factory):
        """Тест успешного поиска вакансий"""
        # Настраиваем моки
        self.ui.hh_api.get_vacancies.return_value = [{'name': 'Python Developer'}]
        mock_input.side_effect = ['Python', '10']

        # Мокаем создание вакансии
        mock_vacancy = MagicMock()
        mock_factory.create_from_hh.return_value = mock_vacancy
        self.ui.vacancies = [mock_vacancy]  # Имитируем заполнение списка

        self.ui.search_vacancies()

        self.ui.hh_api.get_vacancies.assert_called_once_with('Python', 10)
        mock_display.assert_called_once_with([mock_vacancy])

    @patch('src.user_interface.display_vacancies_list')
    def test_show_saved_vacancies_empty(self, mock_display):
        """Тест показа сохраненных вакансий (пустой список)"""
        self.ui.file_manager.get_data.return_value = []

        self.ui.show_saved_vacancies()

        self.ui.file_manager.get_data.assert_called_once()
        mock_display.assert_not_called()

    @patch('src.user_interface.get_user_input')
    def test_clear_all_vacancies_confirmed(self, mock_input):
        """Тест очистки всех вакансий (подтверждено)"""
        mock_input.return_value = 'да'

        self.ui.clear_all_vacancies()

        self.ui.file_manager.clear_all_data.assert_called_once()

    @patch('src.user_interface.get_user_input')
    def test_clear_all_vacancies_cancelled(self, mock_input):
        """Тест очистки всех вакансий (отменено)"""
        mock_input.return_value = 'нет'

        self.ui.clear_all_vacancies()

        self.ui.file_manager.clear_all_data.assert_not_called()

    @patch('src.user_interface.get_user_input')
    @patch('src.user_interface.convert_vacancy_to_dict')
    def test_ask_to_save_vacancies_yes(self, mock_convert, mock_input):
        """Тест подтверждения сохранения вакансий (да)"""
        mock_input.return_value = 'да'
        mock_convert.return_value = {'title': 'Developer'}
        self.ui.vacancies = [MagicMock()]

        self.ui._ask_to_save_vacancies()

        self.ui.file_manager.add_data.assert_called_once()
        mock_convert.assert_called()

    @patch('src.user_interface.get_user_input')
    def test_ask_to_save_vacancies_no(self, mock_input):
        """Тест подтверждения сохранения вакансий (нет)"""
        mock_input.return_value = 'нет'
        self.ui.vacancies = [MagicMock()]

        self.ui._ask_to_save_vacancies()

        self.ui.file_manager.add_data.assert_not_called()

    @patch('src.user_interface.get_user_input')
    def test_ask_to_save_vacancies_empty(self, mock_input):
        """Тест подтверждения сохранения при пустом списке вакансий"""
        self.ui.vacancies = []

        self.ui._ask_to_save_vacancies()

        mock_input.assert_not_called()
        self.ui.file_manager.add_data.assert_not_called()

    @patch('src.user_interface.get_user_input')
    def test_delete_vacancy_success(self, mock_input):
        """Тест успешного удаления вакансии"""
        self.ui.file_manager.get_data.return_value = [
            {'url': 'https://hh.ru/1', 'title': 'Developer'}
        ]
        mock_input.return_value = 'https://hh.ru/1'

        self.ui.delete_vacancy()

        self.ui.file_manager.delete_data.assert_called_once_with({'url': 'https://hh.ru/1'})

    @patch('src.user_interface.get_user_input')
    def test_delete_vacancy_no_saved(self, mock_input):
        """Тест удаления при отсутствии сохраненных вакансий"""
        self.ui.file_manager.get_data.return_value = []

        self.ui.delete_vacancy()

        mock_input.assert_not_called()
        self.ui.file_manager.delete_data.assert_not_called()
