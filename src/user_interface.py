from typing import List

from hh_api import HeadHunterAPI
from json_file_manager import JSONFileManager
from utils import (convert_vacancy_to_dict, display_vacancies_list,
                   format_salary_string, get_user_input)
from vacancy import Vacancy, VacancyFactory


class UserInterface:
    """
    Класс для взаимодействия с пользователем.
    Использует ранее созданные классы без дублирования функциональности.
    """

    def __init__(self):
        """Инициализация интерфейса с необходимыми компонентами."""
        self.hh_api = HeadHunterAPI()
        self.file_manager = JSONFileManager()
        self.vacancies: List[Vacancy] = []

    def _display_welcome_message(self) -> None:
        """Отображает приветственное сообщение."""
        print("=" * 60)
        print("        ПРИЛОЖЕНИЕ ДЛЯ ПОИСКА ВАКАНСИЙ")
        print("=" * 60)
        print()

    def _display_main_menu(self) -> None:
        """Отображает главное меню."""
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1.  Поиск вакансий на HH.ru")
        print("2.  Показать сохраненные вакансии")
        print("3.  Удалить вакансию")
        print("4.  Очистить все сохраненные вакансии")
        print("5.  Выход")
        print()

    def _get_menu_choice(self) -> str:
        """Получает выбор пользователя из меню."""
        return get_user_input("Выберите действие (1-5): ",
                              lambda x: x in ['1', '2', '3', '4', '5'])

    def search_vacancies(self) -> None:
        """Поиск вакансий через HH API."""
        print("\n--- ПОИСК ВАКАНСИЙ ---")
        keyword = get_user_input("Введите ключевое слово для поиска (например 'Python'): ")
        per_page = get_user_input("Сколько вакансий показать (10-100): ",
                                  lambda x: x.isdigit() and 10 <= int(x) <= 100)

        print(f"\nИщем вакансии по запросу: '{keyword}'...")

        try:
            # Используем метод API класса
            vacancies_data = self.hh_api.get_vacancies(keyword, int(per_page))

            if not vacancies_data:
                print("По вашему запросу вакансий не найдено.")
                return

            # Конвертируем данные в объекты Vacancy
            self.vacancies = [VacancyFactory.create_from_hh(data) for data in vacancies_data]

            # Показываем найденные вакансии
            print(f"\nНайдено {len(self.vacancies)} вакансий:")
            display_vacancies_list(self.vacancies)

            # Предлагаем сохранить
            self._ask_to_save_vacancies()

        except Exception as e:
            print(f"Ошибка при поиске вакансий: {e}")

    def _ask_to_save_vacancies(self) -> None:
        """Спрашивает пользователя о сохранении найденных вакансий."""
        if not self.vacancies:
            return

        choice = get_user_input("\nСохранить найденные вакансии? (да/нет): ",
                                lambda x: x.lower() in ['да', 'нет', 'д', 'н', 'yes', 'no', 'y', 'n'])

        if choice.lower() in ['да', 'д', 'yes', 'y']:
            # Конвертируем вакансии в словари для сохранения
            vacancies_dicts = [convert_vacancy_to_dict(vac) for vac in self.vacancies]

            # Используем метод file manager для сохранения
            self.file_manager.add_data(vacancies_dicts)
            print(f" Сохранено {len(vacancies_dicts)} вакансий в файл.")

    def show_saved_vacancies(self) -> None:
        """Показывает сохраненные вакансии."""
        print("\n--- СОХРАНЕННЫЕ ВАКАНСИИ ---")

        # Получаем данные через file manager
        saved_data = self.file_manager.get_data()

        if not saved_data:
            print("У вас нет сохраненных вакансий.")
            return

        # Конвертируем обратно в объекты Vacancy для отображения
        saved_vacancies = []
        for data in saved_data:
            try:
                vacancy = Vacancy(
                    title=data.get('title', ''),
                    url=data.get('url', ''),
                    salary_from=data.get('salary_from', 0),
                    salary_to=data.get('salary_to', 0),
                    currency=data.get('currency', ''),
                    requirements=data.get('requirements', '')
                )
                saved_vacancies.append(vacancy)
            except Exception as e:
                print(f"Ошибка при загрузке вакансии: {e}")
                continue

        display_vacancies_list(saved_vacancies)
        print(f"\nВсего сохранено вакансий: {len(saved_vacancies)}")

    def delete_vacancy(self) -> None:
        """Удаляет вакансию по URL."""
        print("\n--- УДАЛЕНИЕ ВАКАНСИИ ---")

        # Сначала показываем сохраненные вакансии
        saved_data = self.file_manager.get_data()

        if not saved_data:
            print("Нет сохраненных вакансий для удаления.")
            return

        print("Сохраненные вакансии:")
        for i, data in enumerate(saved_data[:10], 1):
            salary_str = format_salary_string(
                data.get('salary_from', 0),
                data.get('salary_to', 0),
                data.get('currency', '')
            )
            print(f"{i}. {data.get('title', 'Без названия')} - {salary_str}")

        # Получаем URL для удаления
        url_to_delete = get_user_input(
            "\nВведите URL вакансии для удаления: ",
            lambda x: x.startswith(('http://', 'https://'))
        )

        # Используем метод file manager для удаления
        self.file_manager.delete_data({'url': url_to_delete})
        print(" Вакансия удалена из сохраненных.")

    def clear_all_vacancies(self) -> None:
        """Очищает все сохраненные вакансии."""
        print("\n--- ОЧИСТКА ВСЕХ ВАКАНСИЙ ---")

        confirmation = get_user_input(
            "Вы уверены, что хотите удалить ВСЕ сохраненные вакансии? (да/нет): ",
            lambda x: x.lower() in ['да', 'нет', 'д', 'н']
        )

        if confirmation.lower() in ['да', 'д']:
            # Используем метод file manager для очистки
            self.file_manager.clear_all_data()
            print(" Все вакансии удалены.")
        else:
            print("Очистка отменена.")

    def run(self) -> None:
        """Основной цикл работы приложения."""
        self._display_welcome_message()

        while True:
            self._display_main_menu()
            choice = self._get_menu_choice()

            if choice == '1':
                self.search_vacancies()
            elif choice == '2':
                self.show_saved_vacancies()
            elif choice == '3':
                self.delete_vacancy()
            elif choice == '4':
                self.clear_all_vacancies()
            elif choice == '5':
                print("\nДо свидания!")
                break

            # Пауза перед следующим действием
            input("\nНажмите Enter чтобы продолжить...")

    def show_vacancy_details(self, vacancy: Vacancy) -> None:
        """
        Показывает детальную информацию о вакансии.

        :param vacancy: Объект вакансии для отображения
        """
        salary_str = format_salary_string(
            vacancy.salary_from,
            vacancy.salary_to,
            vacancy.currency
        )

        print("\n" + "=" * 60)
        print(f"ВАКАНСИЯ: {vacancy.title}")
        print("=" * 60)
        print(f"Зарплата: {salary_str}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Требования: {vacancy.requirements}")
        print("=" * 60)
