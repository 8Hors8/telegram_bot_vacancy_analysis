import random
import re

import datetime
import time

from time import sleep
import requests
from database import Database


def request_api(url: str, params: dict = None):
    """
    Делает запрос в API.
    Возвращает словари 
    """
    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if params is not None:
                vacancies = data.get('items')
            else:
                vacancies = data['rates']['RUB']

        else:
            print('Ошибка при запросе данных:', response.status_code)
            vacancies = 'stop'

        return vacancies
    except requests.exceptions.ConnectionError:
        seconds = 10
        print(f'Ошибка запроса!!! Через {seconds} секунд повторный запрос')
        time.sleep(seconds)
        return request_api(url, params)


def operations_amounts(sum_from: str, sum_to: str, currency: str) -> str:
    """
   Проводит операции над суммами
   :return: str
   """
    if currency == 'RUR':
        if sum_from is not None and sum_to is not None:
            # sum_ = (int(sum_from) + int(sum_to)) / 2
            sum_ = f'{sum_from},{sum_to}'

        elif sum_from is None and sum_to is not None:
            sum_ = f'{sum_to}'

        else:
            sum_ = f'{sum_from}'
    else:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        rub = request_api(url)
        if sum_from is not None and sum_to is not None:
            # sum_ = (int(sum_from) + int(sum_to)) / 2
            sum_ = f'{round(sum_from * rub)},{round(sum_to * rub)}'

        elif sum_from is None and sum_to is not None:
            sum_ = f'{round(sum_to * rub)}'

        else:
            sum_ = f'{round(sum_from * rub)}'

    # return round(sum_)
    return sum_


def analysis_name(name: str) -> list:
    """
    Разбирает name для выявления требуемой классификации разработчиков,
    требуемые framework.
    :param name:
    :return: Список из классификации разработчика и требуемые framework
    """
    framework = ['django', 'cherryPy', 'pyramid', 'turbogears', 'web2Py', 'flask', 'bottle',
                 'tornado', 'web.py', 'fastapi'
                 ]
    developer = ['junior', 'middle', 'senior', 'junior+', 'middle+', 'senior+']
    not_name = ['с++', 'c++', 'php', 'рнр', 'vue', 'преподаватель']
    developer_class = []
    required_framework = []
    permission = True

    split_name = re.split(r'[,:;/ \s]', re.sub(r'[-()|]', ' ', name).lower())

    for el in split_name:
        if el in developer:
            developer_class.append(re.sub(r'[+]', '', el))
        elif el in framework:
            required_framework.append(el)

        if el in not_name:
            permission = False
            break

    return [f'{developer_class}', f'{required_framework}', permission]


def transfers_data_bd(list_vacancies: list):
    """
    Создает и заполняет БД
    :param list_vacancies:
    """
    table_name = 'vacancies'
    columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        'vac_id VARCHAR(200)',
        'name VARCHAR(200)',
        'sum VARCHAR(200)',
        'area VARCHAR(200)',
        'published_at VARCHAR(200)',
        'professional_roles VARCHAR(200)',
        'developer_class VARCHAR(200)',
        'required_framework VARCHAR(200)',
        'date_scan DATE',
    ]

    db = Database()
    db.create_table(table_name, columns)
    filter_columns = ['vac_id']

    vac_id_tuples = db.select_data(table_name, filter_columns)
    vac_id = [item[0] for item in vac_id_tuples]

    for dict_vacancies in list_vacancies:
        if dict_vacancies['vac_id'] not in vac_id:
            db.insert_data(table_name, dict_vacancies)
    db.close_connection()


def sorting_vacancies():
    """
    Запрашивает и обрабатывает вакансии
    :return:
    """
    page_ = 0

    list_vacancies = []
    stop = ''

    while stop != 'stop':

        time_ = random.randint(5, 30)

        url = 'https://api.hh.ru/vacancies'

        params = {
            'text': '!"python developer" OR !"django" OR !"flask" OR !"fastapi"'
                    'NOT DevOps NOT Преподаватель',
            'area': 113,
            'area_id': 113,
            'per_page': 100,
            'page': page_,
            'only_with_salary': True
        }
        vacancies = request_api(url, params)

        # pprint.pprint(vacancies)
        print(f'страница {page_}--------------------------------------------')
        print(len(vacancies))
        print()
        if vacancies != 'stop' and len(vacancies) > 0:
            for vacancy in vacancies:
                name = vacancy.get('name')
                developer_class, required_framework, permission = analysis_name(name)
                id_ = vacancy.get('id')
                sum_ = operations_amounts(vacancy.get('salary').get('from'),
                                          vacancy.get('salary').get('to'),
                                          vacancy.get('salary').get('currency'),

                                          )
                area = [vacancy.get('area').get('id'), vacancy.get('area').get('name')]
                published_at = vacancy.get('published_at').split('T')[0]
                professional_roles = vacancy.get("professional_roles")[0]

                str_vacancy = {
                    'vac_id': id_,
                    'name': name,
                    'sum': sum_,
                    'area': f'{area}',
                    'published_at': published_at,
                    'professional_roles': f'{professional_roles}',
                    'developer_class': developer_class,
                    'required_framework': required_framework,
                    'date_scan': datetime.date.today()
                }
                professional_roles_id = [96, 124, 104]

                if int(professional_roles['id']) in professional_roles_id and permission is True:
                    list_vacancies.append(str_vacancy)

        elif len(vacancies) == 0:
            break
        else:
            stop = vacancies

        page_ += 1

        if len(vacancies) < 100:
            pass
        else:
            sleep(time_)

    transfers_data_bd(list_vacancies)
    return list_vacancies


if __name__ == '__main__':
    v = sorting_vacancies()
    # for r in v:
    #     print(r)
