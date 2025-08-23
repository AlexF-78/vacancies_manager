from typing import Any, Dict, List

from src.csv_file_manager import CSVFileManager
from src.json_file_manager import JSONFileManager
from src.vacancy import Vacancy


class VacancyConverter:
    """Класс для конвертации объектов Vacancy в словари и обратно."""

    @staticmethod
    def vacancies_to_dicts(vacancies: List[Vacancy]) -> List[Dict[str, Any]]:
        """Конвертирует список объектов Vacancy в список словарей."""
        return [
            {
                'title': vacancy.title,
                'url': vacancy.url,
                'salary_from': vacancy.salary_from,
                'salary_to': vacancy.salary_to,
                'currency': vacancy.currency,
                'requirements': vacancy.requirements
            }
            for vacancy in vacancies
        ]

    @staticmethod
    def dicts_to_vacancies(data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Конвертирует список словарей в список объектов Vacancy."""
        return [
            Vacancy(
                title=item['title'],
                url=item['url'],
                salary_from=item['salary_from'],
                salary_to=item['salary_to'],
                currency=item['currency'],
                requirements=item['requirements']
            )
            for item in data
        ]

    # Пример использования:
    # Создаем менеджеры файлов
    json_manager = JSONFileManager("my_vacancies.json")
    csv_manager = CSVFileManager("backup_vacancies.csv")

    # Получаем данные
    vacancies_data = json_manager.get_data()
    print(f"Найдено {len(vacancies_data)} вакансий в JSON файле")

    # Добавляем новые данные
    new_vacancies = [
        {
            'title': 'Python Developer',
            'url': 'https://hh.ru/vacancy/123',
            'salary_from': 100000,
            'salary_to': 150000,
            'currency': 'RUR',
            'requirements': 'Опыт работы 3+ года'
        }
    ]

    json_manager.add_data(new_vacancies)
    csv_manager.add_data(new_vacancies)

    # Удаляем данные по критерию
    json_manager.delete_data({'url': 'https://hh.ru/vacancy/123'})

    # Использование с классом Vacancy
    from vacancy import Vacancy, VacancyFactory

    # Создаем объекты Vacancy
    vacancy = Vacancy(
        title="Java Developer",
        url="https://hh.ru/vacancy/456",
        salary_from=120000,
        salary_to=180000,
        currency="RUR",
        requirements="Знание Spring Framework"
    )

    # Конвертируем в словарь и сохраняем
    vacancy_dict = {
        'title': vacancy.title,
        'url': vacancy.url,
        'salary_from': vacancy.salary_from,
        'salary_to': vacancy.salary_to,
        'currency': vacancy.currency,
        'requirements': vacancy.requirements
    }

    json_manager.add_data([vacancy_dict])
