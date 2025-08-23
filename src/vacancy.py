class Vacancy:
    """
    Класс для представления вакансии.
    Использует __slots__ для экономии памяти.
    """
    __slots__ = ('_title', '_url', '_salary_from', '_salary_to', '_currency', '_requirements')

    def __init__(self, title: str, url: str, salary_from: int | None, salary_to: int | None,
                 currency: str | None, requirements: str):
        """
        Инициализатор вакансии.

        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary_from: Нижняя граница зарплаты
        :param salary_to: Верхняя граница зарплаты
        :param currency: Валюта зарплаты
        :param requirements: Требования/описание вакансии
        """
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = self._validate_currency(currency)
        self._requirements = self._validate_requirements(requirements)

    # region Валидаторы (приватные методы)
    def _validate_title(self, title: str) -> str:
        """Приватный метод валидации названия вакансии."""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Приватный метод валидации URL вакансии."""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL должен начинаться с http:// или https://")
        return url.strip()

    def _validate_salary(self, salary: int | None) -> int:
        """Приватный метод валидации зарплаты."""
        if salary is None:
            return 0
        if not isinstance(salary, int) or salary < 0:
            raise ValueError("Зарплата должна быть положительным целым числом или None")
        return salary

    def _validate_currency(self, currency: str | None) -> str:
        """Приватный метод валидации валюты."""
        if currency is None:
            return "не указана"
        if not isinstance(currency, str):
            raise ValueError("Валюта должна быть строкой")
        return currency.strip().upper()

    def _validate_requirements(self, requirements: str) -> str:
        """Приватный метод валидации требований."""
        if requirements is None:
            return "Не указаны"
        if not isinstance(requirements, str):
            raise ValueError("Требования должны быть строкой")
        return requirements.strip()

    # endregion

    # region Свойства для доступа к приватным атрибутам
    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        return self._salary_from

    @property
    def salary_to(self) -> int:
        return self._salary_to

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def requirements(self) -> str:
        return self._requirements

    # endregion

    # region Методы сравнения по зарплате (магические методы)
    def __lt__(self, other) -> bool:
        """Меньше < (сравниваем по нижней границе зарплаты)"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии с вакансиями")
        return self.salary_from < other.salary_from

    def __le__(self, other) -> bool:
        """Меньше или равно <="""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии с вакансиями")
        return self.salary_from <= other.salary_from

    def __gt__(self, other) -> bool:
        """Больше >"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии с вакансиями")
        return self.salary_from > other.salary_from

    def __ge__(self, other) -> bool:
        """Больше или равно >="""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только вакансии с вакансиями")
        return self.salary_from >= other.salary_from

    def __eq__(self, other) -> bool:
        """Равно =="""
        if not isinstance(other, Vacancy):
            return False
        return self.salary_from == other.salary_from

    # endregion

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_info = ""
        if self.salary_from and self.salary_to:
            salary_info = f"{self.salary_from} - {self.salary_to} {self.currency}"
        elif self.salary_from:
            salary_info = f"от {self.salary_from} {self.currency}"
        elif self.salary_to:
            salary_info = f"до {self.salary_to} {self.currency}"
        else:
            salary_info = "не указана"

        return (f"Вакансия: {self.title}\n"
                f"Зарплата: {salary_info}\n"
                f"Требования: {self.requirements[:100]}...\n"
                f"Ссылка: {self.url}")

    def __repr__(self) -> str:
        """Представление для отладки"""
        return (f"Vacancy(title='{self.title}', salary_from={self.salary_from}, "
                f"salary_to={self.salary_to}, currency='{self.currency}')")


# Фабричный метод для создания вакансий из данных API HH.ru
class VacancyFactory:
    """Класс для создания объектов Vacancy из данных API."""

    @staticmethod
    def create_from_hh(vacancy_data: dict) -> 'Vacancy':
        """
        Создает объект Vacancy из данных API HH.ru.

        :param vacancy_data: Словарь с данными вакансии от HH API
        :return: Объект Vacancy
        """
        # Извлекаем и обрабатываем данные о зарплате
        salary_info = vacancy_data.get('salary')
        salary_from = salary_info.get('from') if salary_info else None
        salary_to = salary_info.get('to') if salary_info else None
        currency = salary_info.get('currency') if salary_info else None

        # Обрабатываем требования (могут быть в разных полях)
        snippet = vacancy_data.get('snippet', {})
        requirements = snippet.get('requirement', '') or snippet.get('responsibility', '')

        return Vacancy(
            title=vacancy_data.get('name', 'Без названия'),
            url=vacancy_data.get('alternate_url', ''),
            salary_from=salary_from,
            salary_to=salary_to,
            currency=currency,
            requirements=requirements or 'Не указаны'
        )


# Пример использования:
# Создаем вакансии
vacancy1 = Vacancy(
    title="Python Developer",
    url="https://hh.ru/vacancy/12345",
    salary_from=100000,
    salary_to=150000,
    currency="RUR",
    requirements="Опыт работы от 3 лет, знание Django, Flask"
)

vacancy2 = Vacancy(
    title="Junior Python Developer",
    url="https://hh.ru/vacancy/67890",
    salary_from=80000,
    salary_to=None,
    currency="RUR",
    requirements="Базовые знания Python"
)

# Используем методы сравнения
print(vacancy1 > vacancy2)   # True (100000 > 80000)
print(vacancy1 <= vacancy2)  # False (100000 <= 80000)
print(vacancy1 == vacancy2)  # False (100000 == 80000)

# Выводим информацию
print("\nВакансия 1:")
print(vacancy1)

print("\nВакансия 2:")
print(vacancy2)

# Использование фабрики (если есть данные от API)
# hh_vacancy_data = {...}  # данные из API HH.ru
# vacancy = VacancyFactory.create_from_hh(hh_vacancy_data)
