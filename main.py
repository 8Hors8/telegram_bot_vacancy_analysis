import concurrent.futures
from job_collector.main_job_collector import sorting_vacancies
from extract_db_df_salaries import extract_salaries, prepare_dataframe
from building_salary_schedules import plot_salaries

if __name__ == '__main__':
    import time

    start = time.time()
    # sorting_vacancies()
    e = extract_salaries(['django', 'junior', 'middle', 'senior'], ['2024-05'])
    r = prepare_dataframe(e)
    plot_salaries(r)
    finish = time.time() - start
    print(finish)
