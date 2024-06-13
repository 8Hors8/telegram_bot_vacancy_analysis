import multiprocessing
from bot.main_bot import main_loop
from job_collector.cron_jobs import start_

if __name__ == '__main__':
    # Создаем два процесса для каждой функции
    process1 = multiprocessing.Process(target=main_loop)
    process2 = multiprocessing.Process(target=start_)

    # Запускаем процессы
    process1.start()
    process2.start()

    # Ожидаем завершения работы каждого процесса
    process1.join()
    process2.join()

    # Выводим сообщение после завершения работы обоих процессов
    print("Работа всех процессов завершена")