import unittest

from src.vacancy import Vacancy
from src.vacancy_converter import VacancyConverter


class TestVacancyConverter(unittest.TestCase):

    def test_vacancies_to_dicts(self):
        """Тест конвертации вакансий в словари"""
        vacancies = [
            Vacancy(
                title="Python Developer",
                url="https://hh.ru/vacancy/123",
                salary_from=100000,
                salary_to=150000,
                currency="RUR",
                requirements="Опыт работы"
            ),
            Vacancy(
                title="Java Developer",
                url="https://hh.ru/vacancy/456",
                salary_from=120000,
                salary_to=None,
                currency="RUR",
                requirements="Знание Spring"
            )
        ]

        result = VacancyConverter.vacancies_to_dicts(vacancies)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], "Python Developer")
        self.assertEqual(result[0]['salary_from'], 100000)
        self.assertEqual(result[1]['title'], "Java Developer")
        self.assertEqual(result[1]['salary_to'], 0)

    def test_dicts_to_vacancies(self):
        """Тест конвертации словарей в вакансии"""
        data = [
            {
                'title': 'Python Developer',
                'url': 'https://hh.ru/vacancy/123',
                'salary_from': 100000,
                'salary_to': 150000,
                'currency': 'RUR',
                'requirements': 'Опыт работы'
            },
            {
                'title': 'Java Developer',
                'url': 'https://hh.ru/vacancy/456',
                'salary_from': 120000,
                'salary_to': None,
                'currency': 'RUR',
                'requirements': 'Знание Spring'
            }
        ]

        result = VacancyConverter.dicts_to_vacancies(data)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Vacancy)
        self.assertEqual(result[0].title, "Python Developer")
        self.assertEqual(result[0].salary_from, 100000)
        self.assertEqual(result[0].salary_to, 150000)
        self.assertEqual(result[1].title, "Java Developer")
        self.assertEqual(result[1].salary_to, 0)

    def test_empty_lists(self):
        """Тест работы с пустыми списками"""
        self.assertEqual(VacancyConverter.vacancies_to_dicts([]), [])
        self.assertEqual(VacancyConverter.dicts_to_vacancies([]), [])
