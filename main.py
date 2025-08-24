import os
import sys

# Добавляем директорию src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.user_interface import UserInterface


def main():
    """
    Основная функция приложения.
    Инициализирует и запускает пользовательский интерфейс.

    :return: None
    """
    try:
        print("Запуск приложения для поиска вакансий...")
        app = UserInterface()
        app.run()
    except KeyboardInterrupt:
        print("\n\nПриложение завершено пользователем.")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        print("Пожалуйста, попробуйте запустить приложение снова.")
    finally:
        print("Работа приложения завершена.")


if __name__ == "__main__":
    main()
