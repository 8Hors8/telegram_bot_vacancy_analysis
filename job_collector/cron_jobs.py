from apscheduler.schedulers.background import BackgroundScheduler
import time
from job_collector.main_job_collector import sorting_vacancies
from job_collector.monthly_patch_analysis import monthly_average_salaries


def start_():
    """
    Запускает функции по расписанию
    """
    scheduler = BackgroundScheduler()

    scheduler.add_job(sorting_vacancies, 'cron', hour=0, minute=0)

    scheduler.add_job(monthly_average_salaries, 'cron', day=1, hour=1, minute=0)

    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        scheduler.shutdown()
if __name__ == '__main__':
    start_()
