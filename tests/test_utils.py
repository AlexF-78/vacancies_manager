import unittest
from unittest.mock import mock_open, patch

from src.utils import (confirm_action, convert_vacancy_to_dict,
                       create_backup_file, display_vacancies_list,
                       filter_data_by_criteria, filter_duplicates_by_url,
                       format_number, format_salary_string, get_user_input,
                       load_json_data, save_json_data, validate_file_exists,
                       validate_salary_values)


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

    @patch("src.utils.get_user_input")
    def test_confirm_action_yes(self, mock_input):
        """Тест подтверждения действия (положительный ответ)"""
        for yes_response in ["да", "д", "yes", "y"]:
            with self.subTest(response=yes_response):
                mock_input.return_value = yes_response
                result = confirm_action("Удалить файл?")
                self.assertTrue(result)

    @patch("src.utils.get_user_input")
    def test_confirm_action_no(self, mock_input):
        """Тест подтверждения действия (отрицательный ответ)"""
        for no_response in ["нет", "н", "no", "n"]:
            with self.subTest(response=no_response):
                mock_input.return_value = no_response
                result = confirm_action("Удалить файл?")
                self.assertFalse(result)

    @patch("src.utils.get_user_input")
    def test_confirm_action_prompt(self, mock_input):
        """Тест, что prompt передается корректно"""
        mock_input.return_value = "да"
        confirm_action("Тестовый вопрос?")

        # Проверяем первый аргумент (prompt)
        args, kwargs = mock_input.call_args
        self.assertEqual(args[0], "Тестовый вопрос? (да/нет): ")

        # Проверяем что второй аргумент - функция валидации
        self.assertTrue(callable(args[1]))

    # Тесты для validate_file_exists
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_validate_file_exists_json(self, mock_file, mock_exists):
        """Тест создания JSON файла если не существует"""
        mock_exists.return_value = False

        validate_file_exists("test.json")

        mock_file.assert_called_with("test.json", "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called()  # Проверяем что write вызывался

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_validate_file_exists_txt(self, mock_file, mock_exists):
        """Тест создания текстового файла если не существует"""
        mock_exists.return_value = False

        validate_file_exists("test.txt")

        mock_file.assert_called_with("test.txt", "w", encoding="utf-8")

    # Тесты для filter_duplicates_by_url
    def test_filter_duplicates_by_url_no_duplicates(self):
        """Тест фильтрации без дубликатов"""
        new_data = [{"url": "https://hh.ru/3"}, {"url": "https://hh.ru/4"}]
        existing_data = [{"url": "https://hh.ru/1"}, {"url": "https://hh.ru/2"}]

        result = filter_duplicates_by_url(new_data, existing_data)
        self.assertEqual(len(result), 2)

    def test_filter_duplicates_by_url_with_duplicates(self):
        """Тест фильтрации с дубликатами"""
        new_data = [{"url": "https://hh.ru/1"}, {"url": "https://hh.ru/4"}]
        existing_data = [{"url": "https://hh.ru/1"}, {"url": "https://hh.ru/2"}]

        result = filter_duplicates_by_url(new_data, existing_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["url"], "https://hh.ru/4")

    # Тесты для load_json_data
    @patch("builtins.open", new_callable=mock_open, read_data='[{"test": "data"}]')
    def test_load_json_data_success(self, mock_file):
        """Тест успешной загрузки JSON данных"""
        result = load_json_data("test.json")
        self.assertEqual(result, [{"test": "data"}])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_json_data_file_not_found(self, mock_file):
        """Тест загрузки при отсутствии файла"""
        result = load_json_data("test.json")
        self.assertEqual(result, [])

    # Тесты для save_json_data
    @patch("builtins.open", new_callable=mock_open)
    def test_save_json_data_success(self, mock_file):
        """Тест успешного сохранения JSON данных"""
        test_data = [{"name": "Test", "value": 123}]
        save_json_data("test.json", test_data)
        mock_file.assert_called_with("test.json", "w", encoding="utf-8")

    # Тесты для filter_data_by_criteria
    def test_filter_data_by_criteria(self):
        """Тест фильтрации данных по критериям"""
        data = [
            {"name": "John", "age": 25},
            {"name": "Jane", "age": 30},
            {"name": "John", "age": 35},
        ]

        # Функция УДАЛЯЕТ элементы, соответствующие критериям
        result = filter_data_by_criteria(data, {"name": "John"})
        self.assertEqual(len(result), 1)  # Остается только Jane
        self.assertEqual(result[0]["name"], "Jane")  # John'ы удалены
        self.assertEqual(result[0]["age"], 30)

    def test_filter_data_by_criteria_no_match(self):
        """Тест фильтрации когда нет совпадений"""
        # data = [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]

    # Тесты для convert_vacancy_to_dict
    def test_convert_vacancy_to_dict(self):
        """Тест конвертации вакансии в словарь"""
        from src.vacancy import Vacancy

        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            requirements="Опыт работы",
        )

        result = convert_vacancy_to_dict(vacancy)

        # Проверяем отдельные поля вместо полного сравнения словарей
        self.assertEqual(result["title"], "Python Developer")
        self.assertEqual(result["url"], "https://hh.ru/vacancy/123")
        self.assertEqual(result["salary_from"], 100000)
        self.assertEqual(result["salary_to"], 150000)
        self.assertEqual(result["currency"], "RUR")
        self.assertEqual(result["requirements"], "Опыт работы")

        # Проверяем что date_created добавлен и является строкой
        self.assertIn("date_created", result)
        self.assertIsInstance(result["date_created"], str)

    # Тесты для validate_salary_values
    def test_validate_salary_values_both_valid(self):
        """Тест валидации обеих границ зарплаты"""
        result = validate_salary_values(100000, 150000)
        self.assertEqual(result, (100000, 150000))

    def test_validate_salary_values_swap_if_wrong_order(self):
        """Тест автоматического обмена если from > to"""
        result = validate_salary_values(150000, 100000)
        self.assertEqual(result, (100000, 150000))

    def test_validate_salary_values_none_values(self):
        """Тест валидации None значений"""
        result = validate_salary_values(None, None)
        self.assertEqual(result, (0, 0))

    # Тесты для format_salary_string
    def test_format_salary_string_both_values(self):
        """Тест форматирования строки зарплаты с обеими границами"""
        result = format_salary_string(100000, 150000, "RUR")
        self.assertEqual(result, "100000 - 150000 RUR")

    def test_format_salary_string_only_from(self):
        """Тест форматирования только с нижней границей"""
        result = format_salary_string(100000, 0, "USD")
        self.assertEqual(result, "от 100000 USD")

    def test_format_salary_string_only_to(self):
        """Тест форматирования только с верхней границей"""
        result = format_salary_string(0, 150000, "EUR")
        self.assertEqual(result, "до 150000 EUR")

    def test_format_salary_string_none(self):
        """Тест форматирования без зарплаты"""
        result = format_salary_string(0, 0, "")
        self.assertEqual(result, "не указана")

    def test_format_salary_string(self):
        """Тест форматирования строки зарплаты"""
        # Тест с обеими границами зарплаты
        result = format_salary_string(100000, 150000, "RUR")
        self.assertEqual(result, "100000 - 150000 RUR")

        # Тест только с нижней границей
        result = format_salary_string(100000, None, "RUR")
        self.assertEqual(result, "от 100000 RUR")

        # Тест только с верхней границей
        result = format_salary_string(None, 150000, "USD")
        self.assertEqual(result, "до 150000 USD")

        # Тест без зарплаты
        result = format_salary_string(None, None, None)
        self.assertEqual(result, "не указана")

        # Тест с нулевыми значениями - теперь должно быть "не указана"
        result = format_salary_string(0, 0, "EUR")
        self.assertEqual(result, "не указана")

    def test_format_salary_string_edge_cases(self):
        """Тест пограничных случаев форматирования зарплаты"""
        # Зарплата от 0 до X
        result = format_salary_string(0, 50000, "RUR")
        self.assertEqual(result, "до 50000 RUR")

        # Зарплата от X до 0
        result = format_salary_string(100000, 0, "USD")
        self.assertEqual(result, "от 100000 USD")

        # Обе границы 0
        result = format_salary_string(0, 0, "EUR")
        self.assertEqual(result, "не указана")

    @patch("builtins.print")
    def test_display_vacancies_list_with_data(self, mock_print):
        """Тест отображения списка вакансий"""
        from src.vacancy import Vacancy

        vacancies = [
            Vacancy("Dev", "https://hh.ru/1", 100000, 150000, "RUR", "Requirements"),
            Vacancy("Test", "https://hh.ru/2", 80000, None, "USD", "Test requirements"),
        ]

        display_vacancies_list(vacancies)
        self.assertGreater(
            mock_print.call_count, 2
        )  # Должно быть несколько вызовов print

    # Тесты для get_user_input
    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_user_input_valid(self, mock_print, mock_input):
        """Тест получения валидного ввода"""
        mock_input.return_value = "test"
        result = get_user_input("Введите: ")
        self.assertEqual(result, "test")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_user_input_with_validation(self, mock_print, mock_input):
        """Тест получения ввода с валидацией"""
        mock_input.side_effect = ["invalid", "valid"]

        def validation_func(x):
            return x == "valid"

        result = get_user_input("Введите: ", validation_func)
        self.assertEqual(result, "valid")
        self.assertEqual(mock_input.call_count, 2)

    # Тесты для display_vacancies_list
    @patch("builtins.print")
    def test_display_vacancies_list_empty(self, mock_print):
        """Тест отображения пустого списка"""
        display_vacancies_list([])
        mock_print.assert_called_with("Вакансии не найдены.")

    # Тесты для create_backup_file
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("datetime.datetime")
    def test_create_backup_file(self, mock_datetime, mock_file, mock_exists):
        """Тест создания резервной копии"""
        mock_exists.return_value = True
        mock_datetime.now.return_value.strftime.return_value = "20231201_120000"

        # Мокируем успешное выполнение
        with patch("json.load", return_value=[]), patch("json.dump") as mock_dump:
            result = create_backup_file("test.json")
            mock_dump.assert_called_once()
            self.assertTrue(result)  # Проверяем что возвращается непустая строка
            self.assertIn("backup_", result)
