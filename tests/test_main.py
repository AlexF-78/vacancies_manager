import unittest
from unittest.mock import MagicMock, patch

from main import main


class TestMain(unittest.TestCase):

    @patch('main.UserInterface')
    @patch('main.print')
    def test_main_normal_execution(self, mock_print, mock_ui):
        """Тест нормального выполнения main"""
        mock_app = MagicMock()
        mock_ui.return_value = mock_app

        main()

        mock_ui.assert_called_once()
        mock_app.run.assert_called_once()
        mock_print.assert_any_call("Работа приложения завершена.")

    @patch('main.UserInterface')
    @patch('main.print')
    def test_main_keyboard_interrupt(self, mock_print, mock_ui):
        """Тест завершения по Ctrl+C"""
        mock_app = MagicMock()
        mock_ui.return_value = mock_app
        mock_app.run.side_effect = KeyboardInterrupt()

        main()

        mock_print.assert_any_call("\n\nПриложение завершено пользователем.")
        mock_print.assert_any_call("Работа приложения завершена.")

    @patch('main.UserInterface')
    @patch('main.print')
    def test_main_general_exception(self, mock_print, mock_ui):
        """Тест обработки общего исключения"""
        mock_app = MagicMock()
        mock_ui.return_value = mock_app
        mock_app.run.side_effect = Exception("Test error")

        main()

        mock_print.assert_any_call("\nПроизошла непредвиденная ошибка: Test error")
        mock_print.assert_any_call("Работа приложения завершена.")
