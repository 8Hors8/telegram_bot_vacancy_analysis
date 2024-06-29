"""Преобразует данные из БД в DataFrame """
from generating_queries_database import formation_filters as ff
import pandas as pd


def extract_salaries(filter_: dict):
    """
    Рекурсивно извлекает все зарплаты из вложенных словарей и списков.
    Возвращает словарь с ключами и зарплатами.

    :param filter_: dict {
                    'filter':list пример [django, middle, senior],
                    'datas': list ['дата от','дата до'] пример ['2024-03', '2024-04'],
                    'city': str например 'Москва'
                     }
    :return: dict ключ состоящий из элементов 'filter' и заплат
    """
    filter_query = filter_['filter']
    datas_ = filter_['datas']
    city = filter_['city']

    data_list = ff(query_=filter_query, dates_=datas_, city=city)

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
        'position': positions,
        'min': min_salaries,
        'mean': mean_salaries,
        'max': max_salaries
    }

    return pd.DataFrame(data)
