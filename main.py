"""
Главный модуль для запуска Telegram бота и выполнения вспомогательных задач.

Этот модуль включает в себя функции для инициализации и запуска бота Telegram
в двух процессах с использованием библиотеки multiprocessing. Он также загружает
переменные окружения из файла token.env для получения API токена Telegram.

Функции:
- `main()`: Основная функция, которая инициализирует и запускает два процесса:
  один для запуска бота Telegram и другой для выполнения других задач.
- `run_bot(token)`: Функция для инициализации и запуска Telegram бота с указанным токеном.

Для успешной работы необходимо наличие файла token.env с указанием переменной окружения
BOT_API_TOKEN, содержащей токен для доступа к API Telegram.

Пример использования:
    Запустите функцию `main()` для запуска всех процессов и бота Telegram.

Ограничения:
    - Требуется поддержка метода 'spawn' для создания процессов (для Unix-подобных систем).
    - Необходимо установить библиотеку python-dotenv для загрузки переменных окружения из файла.

Автор: [Hors]
Дата создания: [2024-07-24]
"""
import multiprocessing
import os
from dotenv import load_dotenv
from job_collector.cron_jobs import start_


def main():
    """
       Функция для запуска бота Telegram в двух процессах.

       Использует метод 'spawn' для создания новых процессов с помощью multiprocessing.
       Загружает переменные окружения из файла token.env и проверяет наличие API токена.
       Запускает два процесса: один для запуска бота Telegram, другой для выполнения других задач.
       Ожидает завершения работы каждого процесса и выводит сообщение после их завершения.

       Raises:
           ValueError: Если переменная окружения BOT_API_TOKEN не указана в файле token.env.
       """
    # Используем метод spawn для создания новых процессов
    multiprocessing.set_start_method('spawn')

    # Загружаем переменные окружения из файла token.env
    load_dotenv(dotenv_path='./bot/token.env')

    api_token = os.getenv('BOT_API_TOKEN')
    if not api_token:
        raise ValueError("Токен API не предоставлен. Установите BOT_API_TOKEN в файле token.env")

    # Создаем и запускаем два процесса
    process1 = multiprocessing.Process(target=run_bot, args=(api_token,))
    process2 = multiprocessing.Process(target=start_)

    # Запускаем процессы
    process1.start()
    process2.start()

    # Ожидаем завершения работы каждого процесса
    process1.join()
    process2.join()

    # Выводим сообщение после завершения работы обоих процессов
    print("Работа всех процессов завершена")


def run_bot(token):
    """
        Функция для запуска Telegram бота.

        Args:
            token (str): Токен для доступа к API Telegram.

        Запускает экземпляр TelegramBot с указанным токеном и запускает его метод run().
        """
    import asyncio
    from bot.main_bot import TelegramBot
    bot = TelegramBot(token)
    asyncio.run(bot.run())


if __name__ == '__main__':
    main()
