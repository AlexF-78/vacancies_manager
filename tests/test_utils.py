import unittest
from unittest.mock import patch

from src.utils import confirm_action, format_number


class TestUtils(unittest.TestCase):

    def test_format_number(self):
        """Тест форматирования чисел"""
        self.assertEqual(format_number(1000), "1 000")
        self.assertEqual(format_number(1234567), "1 234 567")
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(999), "999")
        self.assertEqual(format_number(1000000), "1 000 000")

    def test_format_number_negative(self):
        """Тест форматирования отрицательных чисел"""
        self.assertEqual(format_number(-1000), "-1 000")
        self.assertEqual(format_number(-1234567), "-1 234 567")

    @patch('src.utils.get_user_input')
    def test_confirm_action_yes(self, mock_input):
        """Тест подтверждения действия (положительный ответ)"""
        for yes_response in ['да', 'д', 'yes', 'y']:
            with self.subTest(response=yes_response):
                mock_input.return_value = yes_response
                result = confirm_action("Удалить файл?")
                self.assertTrue(result)

    @patch('src.utils.get_user_input')
    def test_confirm_action_no(self, mock_input):
        """Тест подтверждения действия (отрицательный ответ)"""
        for no_response in ['нет', 'н', 'no', 'n']:
            with self.subTest(response=no_response):
                mock_input.return_value = no_response
                result = confirm_action("Удалить файл?")
                self.assertFalse(result)

    @patch('src.utils.get_user_input')
    def test_confirm_action_prompt(self, mock_input):
        """Тест, что prompt передается корректно"""
        mock_input.return_value = 'да'
        confirm_action("Тестовый вопрос?")

        # Проверяем первый аргумент (prompt)
        args, kwargs = mock_input.call_args
        self.assertEqual(args[0], "Тестовый вопрос? (да/нет): ")

        # Проверяем что второй аргумент - функция валидации
        self.assertTrue(callable(args[1]))
