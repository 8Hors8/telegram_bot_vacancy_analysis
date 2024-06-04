import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from generating_queries_database import formation_filters as ff


def extract_salaries(filter_: list, datas_=None, city=None):
    """
    Рекурсивно извлекает все зарплаты из вложенных словарей и списков.
    Возвращает словарь с ключами и зарплатами.

    :param filter_: list
    :param datas_: list ['дата от','дата до'] пример ['2024-03', '2024-04']
    :param city: str
    :return:
    """
    data_list = ff(query_=filter_, dates_=datas_, city=city)

    salaries_dict = {}

    def recursive_extract(data, key_path=''):
        """
        Формирует словарь со значениями
        :param data:
        :param key_path:
        """
        if isinstance(data, dict):
            for key, value in data.items():
                new_key_path = f"{key_path}/{key}" if key_path else key
                recursive_extract(value, new_key_path)
        elif isinstance(data, list):
            for item in data:
                recursive_extract(item, key_path)
        elif isinstance(data, int):
            if key_path in salaries_dict:
                salaries_dict[key_path].append(data)
            else:
                salaries_dict[key_path] = [data]

    recursive_extract(data_list)
    return salaries_dict


def prepare_dataframe(salaries_dict):
    """
    Преобразует словарь с зарплатами в DataFrame с колонками 'Позиция', 'Min', 'Mean', 'Max'.
    """
    positions = []
    min_salaries = []
    mean_salaries = []
    max_salaries = []

    for key, salaries in salaries_dict.items():
        positions.append(key)
        min_salaries.append(min(salaries) / 1000)
        mean_salaries.append(int((sum(salaries) / len(salaries)) / 1000))
        max_salaries.append(max(salaries) / 1000)

    data = {
        'Позиция': positions,
        'Min': min_salaries,
        'Mean': mean_salaries,
        'Max': max_salaries
    }

    return pd.DataFrame(data)


def plot_salaries(df):
    """
    Строит график зарплат.
    """
    plt.figure(figsize=(12, 5))
    sns.set(style="whitegrid")

    for index, row in df.iterrows():
        plt.plot([row['Min'], row['Max']], [index, index], 'o-', color='red')
        plt.scatter(row['Mean'], index, color='blue', zorder=3)

    plt.yticks(range(len(df)), df['Позиция'])
    plt.gca().invert_yaxis()
    plt.xlabel('Зарплата (тыс. рублей)')
    plt.title('Анализ зарплат')
    plt.show()


if __name__ == '__main__':
    e = extract_salaries(['django', 'junior', 'middle', 'fastapi', 'senior'])
    r = prepare_dataframe(e)
    plot_salaries(r)
