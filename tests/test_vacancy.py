import unittest

from src.vacancy import Vacancy, VacancyFactory


class TestVacancy(unittest.TestCase):

    def test_vacancy_creation_valid(self):
        """Тест создания вакансии с валидными данными"""
        vacancy = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            requirements="Опыт работы 3+ года"
        )

        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.currency, "RUR")
        self.assertEqual(vacancy.requirements, "Опыт работы 3+ года")

    def test_vacancy_creation_none_salary(self):
        """Тест создания вакансии с None зарплатой"""
        vacancy = Vacancy(
            title="Developer",
            url="https://hh.ru/vacancy/456",
            salary_from=None,
            salary_to=None,
            currency=None,
            requirements="Требования"
        )

        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)
        self.assertEqual(vacancy.currency, "не указана")

    def test_vacancy_comparison(self):
        """Тест сравнения вакансий по зарплате"""
        vacancy1 = Vacancy("A", "https://a.com", 100000, None, "RUR", "req")
        vacancy2 = Vacancy("B", "https://b.com", 80000, None, "RUR", "req")

        self.assertTrue(vacancy1 > vacancy2)
        self.assertTrue(vacancy2 < vacancy1)
        self.assertTrue(vacancy1 >= vacancy2)
        self.assertTrue(vacancy2 <= vacancy1)
        self.assertFalse(vacancy1 == vacancy2)

    def test_vacancy_str_representation(self):
        """Тест строкового представления вакансии"""
        vacancy = Vacancy(
            title="Python Dev",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            requirements="Опыт работы"
        )

        str_repr = str(vacancy)
        self.assertIn("Python Dev", str_repr)
        self.assertIn("100000 - 150000 RUR", str_repr)
        self.assertIn("https://hh.ru/vacancy/123", str_repr)


class TestVacancyFactory(unittest.TestCase):

    def test_create_from_hh_valid_data(self):
        """Тест создания вакансии из данных HH"""
        hh_data = {
            'name': 'Python Developer',
            'alternate_url': 'https://hh.ru/vacancy/123',
            'salary': {
                'from': 100000,
                'to': 150000,
                'currency': 'RUR'
            },
            'snippet': {
                'requirement': 'Опыт работы 3 года',
                'responsibility': 'Разработка приложений'
            }
        }

        vacancy = VacancyFactory.create_from_hh(hh_data)

        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.currency, "RUR")
        self.assertEqual(vacancy.requirements, "Опыт работы 3 года")

    def test_create_from_hh_no_salary(self):
        """Тест создания вакансии из данных HH без зарплаты"""
        hh_data = {
            'name': 'Developer',
            'alternate_url': 'https://hh.ru/vacancy/456',
            'salary': None,
            'snippet': {
                'requirement': None,
                'responsibility': 'Разработка'
            }
        }

        vacancy = VacancyFactory.create_from_hh(hh_data)

        self.assertEqual(vacancy.title, "Developer")
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)
        self.assertEqual(vacancy.currency, "не указана")
        self.assertEqual(vacancy.requirements, "Разработка")
