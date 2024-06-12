import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from database import Database


def plot_salaries(df):
    """
    Строит график зарплат из таблицы vacancies с большим набором фильтров
    :param df: принимает dataframe из функции prepare_dataframe
    """
    plt.figure(figsize=(12, 5))
    sns.set(style="whitegrid")

    for index, row in df.iterrows():
        plt.plot([row['min'], row['max']], [index, index], 'o-', color='red')
        plt.scatter(row['mean'], index, color='blue', zorder=3)

    plt.yticks(range(len(df)), df['position'])
    plt.gca().invert_yaxis()
    plt.xlabel('Зарплата (тыс. рублей)')
    plt.title('Анализ зарплат')
    plt.show()


def monthly_salary_plot(filter_: dict):
    """
    Строит график медианной заплаты по месяцам
    :param filter_: dict {'filter':str'условие фильтрации','city':str'город'}
    """

    def query_sql(filter_d: dict):
        """
        Формирут запрос в бд
        :param filter_d: Фильтр
        :return: список из бд
        """
        table_name = 'salaryinsights'
        filter_columns = ['position', 'mean', 'date']

        if filter_d['filter'] == 'python developer':
            str_query = f"""city LIKE '%{filter_d['city']}%' AND position NOT LIKE '%django%' """
            conditions = f'WHERE {str_query}'

        elif filter_d['filter'] == 'django':
            str_query = f"""position LIKE '%{filter_d['filter']}%' AND
             city LIKE '%{filter_d['city']}%'"""
            conditions = f'WHERE {str_query}'

        db = Database()
        db_mean = db.select_data(table_name, filter_columns, conditions)
        return db_mean

    def formation_df(db_mean: list):
        """
        Формирует DataFrame для построения
        :param db_mean: список из бд
        :return: DataFrame
        """
        data = {'period': []}
        for el in db_mean:
            key = el[0]
            mean = el[1]
            date = el[2]

            if key not in data:
                data[key] = [mean]
            else:
                data[key].append(mean)

            if date not in data['period']:
                data['period'].append(date)
        return pd.DataFrame(data)

    df = formation_df(query_sql(filter_))

    sns.set(style="whitegrid")

    plt.figure(figsize=(12, 6))

    for column in df.columns[1:]:
        plt.plot(df['period'], df[column], marker='d', label=column)

    for i, row in df.iterrows():
        for column in df.columns[1:]:
            plt.text(row['period'], row[column], f'{row[column]}К',
                     color='black', ha='center', va='bottom', fontsize=9)

    plt.xlabel('')
    plt.ylabel('Зарплата (тыс. рублей)')
    plt.title(f"""Средняя заплата по месяцам ({filter_['filter']})""")
    plt.legend(title='', loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    monthly_salary_plot({'filter': 'django', 'city': 'Москва'})
