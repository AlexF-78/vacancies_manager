from abc import ABC
from unittest.mock import Mock, patch

import pytest
import requests

from src.abstract_api import AbstractAPI


class TestAbstractAPI:
    """Основные тесты для AbstractAPI"""

    def test_is_abstract_class(self):
        """Тест, что класс является абстрактным"""
        assert issubclass(AbstractAPI, ABC)

    def test_cannot_instantiate_directly(self):
        """Тест, что нельзя создать экземпляр абстрактного класса"""
        with pytest.raises(TypeError):
            AbstractAPI()

    def test_has_required_abstract_methods(self):
        """Тест наличия обязательных абстрактных методов"""
        assert hasattr(AbstractAPI, '__init__')
        assert hasattr(AbstractAPI, '_connect')
        assert hasattr(AbstractAPI, 'get_vacancies')

    def test_concrete_class_must_implement_all_methods(self):
        """Тест, что потомок должен реализовать все методы"""
        # Неполная реализация
        with pytest.raises(TypeError):
            class IncompleteAPI(AbstractAPI):
                def __init__(self):
                    self._base_url = "https://api.hh.ru/vacancies"

                def get_vacancies(self, keyword: str, per_page: int = 100):
                    return []

            IncompleteAPI()


class ConcreteAPI(AbstractAPI):
    """Конкретная реализация для тестирования"""

    def __init__(self):
        super().__init__()
        self._base_url = "https://api.hh.ru/vacancies"

    def _connect(self):
        #  Реализация абстрактного метода
        return requests.get(self._base_url, timeout=10)

    def get_vacancies(self, keyword: str, per_page: int = 100):
        return [{"title": f"{keyword} developer", "url": "https://api.hh.ru/vacancies"}]


def test_concrete_api_implementation():
    """Тест успешной реализации абстрактного класса"""
    api = ConcreteAPI()
    assert isinstance(api, AbstractAPI)
    assert api._base_url == "https://api.hh.ru/vacancies"


@patch(__name__ + '.requests')
def test_connect_method(mock_requests):
    """Тест метода _connect"""
    mock_response = Mock()
    mock_requests.get.return_value = mock_response

    api = ConcreteAPI()
    result = api._connect()

    mock_requests.get.assert_called_once_with("https://api.hh.ru/vacancies", timeout=10)
    assert result == mock_response


def test_get_vacancies_method():
    """Тест метода get_vacancies"""
    api = ConcreteAPI()
    vacancies = api.get_vacancies("python", 50)

    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "python developer"
