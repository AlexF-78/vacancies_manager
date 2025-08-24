from typing import Any, Dict, List

# from src.json_file_manager import JSONFileManager
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
        vacancies = []
        for item in data:
            try:
                vacancy = Vacancy(
                    title=item.get('title', ''),
                    url=item.get('url', ''),
                    salary_from=item.get('salary_from', 0),
                    salary_to=item.get('salary_to', 0),
                    currency=item.get('currency', 'Не указана'),
                    requirements=item.get('requirements', 'Не указаны')
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue
        return vacancies
