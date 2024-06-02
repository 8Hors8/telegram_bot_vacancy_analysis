import concurrent.futures
from job_collector.main_job_collector import sorting_vacancies
from bot.salary_analysis import extract_salaries, prepare_dataframe, plot_salaries
import time

if __name__ == '__main__':
    start = time.time()
    # sorting_vacancies()
    e = extract_salaries(['python developer','django', 'junior', 'middle', 'fastapi', 'senior'])
    r = prepare_dataframe(e)
    plot_salaries(r)
    finish = time.time() - start
    print(finish)
