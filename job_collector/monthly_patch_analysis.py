import datetime
import time

from sqlalchemy import create_engine
from extract_db_df_salaries import extract_salaries as extract_sal
from extract_db_df_salaries import prepare_dataframe as prepare_df


def monthly_average_salaries():
    """
    Создает новую таблицу и добавляет медианную заплату в бд
    """
    date = receipt_previous_month()
    cities = ['Москва', 'Новосибирск']
    filters_ = [['junior', 'middle', 'senior'], ['django', 'junior', 'middle', 'senior']]
    for city in cities:
        for el in filters_:
            list_patches = extract_sal(filter_=el, datas_=[f'{date}'], city=city)
            if list_patches:
                df = prepare_df(list_patches)
                df['date'] = date
                df['city'] = city
                db_engine = create_engine('sqlite:///JobMarketDB.db')
                df[['position', 'mean', 'date', 'city']].to_sql('salaryinsights',
                                                                db_engine, if_exists='append', index=False)


def receipt_previous_month():
    """
    Вычисляет предыдущий месяц
    :return: строку с датой
    """
    current_date = datetime.date.today()
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
    year = last_day_of_previous_month.year
    month = last_day_of_previous_month.month
    formatted_date = f"{year}-{month:02d}"
    return formatted_date


if __name__ == '__main__':
    start = time.time()
    monthly_average_salaries()
    end_ = time.time() - start
    print(end_)
