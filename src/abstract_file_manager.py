from abc import ABC, abstractmethod


class AbstractFileManager(ABC):
    """
    Абстрактный класс для работы с файлами данных.
    Определяет интерфейс для всех классов-менеджеров файлов.
    """

    @abstractmethod
    def __init__(self, filename: str):
        self._filename = filename

    @abstractmethod
    def get_data(self):
        """
        Абстрактный метод для получения данных из файла.
        :return: Данные из файла
        """
        pass

    @abstractmethod
    def add_data(self, data):
        """
        Абстрактный метод для добавления данных в файл.
        :param data: Данные для добавления
        """
        pass

    @abstractmethod
    def delete_data(self, criteria):
        """
        Абстрактный метод для удаления данных из файла.
        :param criteria: Критерий для удаления данных
        """
        pass
