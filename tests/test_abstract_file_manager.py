import unittest
from abc import ABC

from src.abstract_file_manager import AbstractFileManager


class TestAbstractFileManager(unittest.TestCase):
    """Тесты для AbstractFileManager"""

    def test_class_is_abstract(self):
        """Проверяем, что класс является абстрактным"""
        self.assertTrue(issubclass(AbstractFileManager, ABC))

        # Нельзя создать экземпляр абстрактного класса
        with self.assertRaises(TypeError):
            AbstractFileManager("test.txt")

    def test_has_required_methods(self):
        """Проверяем наличие обязательных методов"""
        required_methods = ['get_data', 'add_data', 'delete_data']

        for method_name in required_methods:
            self.assertTrue(hasattr(AbstractFileManager, method_name))

    def test_init_has_filename_parameter(self):
        """Проверяем, что __init__ принимает filename"""

        # Создаем mock-реализацию для проверки
        class TestImplementation(AbstractFileManager):
            def __init__(self, filename: str):
                super().__init__(filename)
                self.filename = filename

            def get_data(self):
                pass

            def add_data(self, data):
                pass

            def delete_data(self, criteria):
                pass

        # Проверяем, что filename сохраняется
        test_file = "test.txt"
        implementation = TestImplementation(test_file)
        self.assertEqual(implementation.filename, test_file)
