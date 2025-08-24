import unittest
from unittest.mock import patch

from src.json_file_manager import JSONFileManager


class TestJSONFileManager(unittest.TestCase):

    @patch("src.json_file_manager.validate_file_exists")
    def setUp(self, mock_validate):
        """Подготовка тестового окружения"""
        mock_validate.return_value = None
        self.manager = JSONFileManager("test.json")

    @patch("src.json_file_manager.load_json_data")
    def test_get_data(self, mock_load):
        """Тест получения данных"""
        mock_data = [{"id": 1, "name": "test"}]
        mock_load.return_value = mock_data

        result = self.manager.get_data()
        self.assertEqual(result, mock_data)
        mock_load.assert_called_once_with("test.json")

    @patch("src.json_file_manager.load_json_data")
    @patch("src.json_file_manager.filter_duplicates_by_url")
    @patch("src.json_file_manager.save_json_data")
    def test_add_data(self, mock_save, mock_filter, mock_load):
        """Тест добавления данных"""
        mock_load.return_value = [{"id": 1}]
        mock_filter.return_value = [{"id": 2}]

        self.manager.add_data([{"id": 2}])

        mock_filter.assert_called_once_with([{"id": 2}], [{"id": 1}])
        mock_save.assert_called_once_with("test.json", [{"id": 1}, {"id": 2}])

    @patch("src.json_file_manager.load_json_data")
    @patch("src.json_file_manager.filter_duplicates_by_url")
    @patch("src.json_file_manager.save_json_data")
    def test_add_empty_data(self, mock_save, mock_filter, mock_load):
        """Тест добавления пустых данных"""
        self.manager.add_data([])
        mock_save.assert_not_called()
        mock_filter.assert_not_called()

    @patch("src.json_file_manager.create_backup_file")
    @patch("src.json_file_manager.load_json_data")
    @patch("src.json_file_manager.filter_data_by_criteria")
    @patch("src.json_file_manager.save_json_data")
    def test_delete_data(self, mock_save, mock_filter, mock_load, mock_backup):
        """Тест удаления данных"""
        mock_load.return_value = [{"id": 1}, {"id": 2}]
        mock_filter.return_value = [{"id": 1}]
        mock_backup.return_value = "/backup/test.json.bak"

        self.manager.delete_data({"id": 2})

        mock_backup.assert_called_once_with("test.json")
        mock_filter.assert_called_once_with([{"id": 1}, {"id": 2}], {"id": 2})
        mock_save.assert_called_once_with("test.json", [{"id": 1}])

    @patch("src.json_file_manager.save_json_data")
    def test_clear_all_data(self, mock_save):
        """Тест очистки всех данных"""
        self.manager.clear_all_data()
        mock_save.assert_called_once_with("test.json", [])
