import multiprocessing
import os
from dotenv import load_dotenv
from job_collector.cron_jobs import start_

def main():
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
    import asyncio
    from bot.main_bot import TelegramBot
    bot = TelegramBot(token)
    asyncio.run(bot.run())

if __name__ == '__main__':
    main()