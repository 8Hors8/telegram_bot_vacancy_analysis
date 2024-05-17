import random
import re
import pprint
import requests

from time import sleep
from database import Database


def unloading_vacancies(page_: int) -> dict | str:
    """
    Делает запрос в API hh.ru.
    Возвращает словари с вакансиями
    """
    url = 'https://api.hh.ru/vacancies'

    params = {'text': '!"python developer" not c++ not c#',
              'area': 1,
              'area_id': 113,
              'per_page': 100,
              'page': page_,
              'only_with_salary': True
              }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get('items')

    else:
        print('Ошибка при запросе данных:', response.status_code)
        vacancies = 'stop'

    return vacancies


def operations_amounts(sum_from: str, sum_to: str) -> str:
    """
   Проводит операции над суммами
   :return: init
   """
    if sum_from is not None and sum_to is not None:
        # sum_ = (int(sum_from) + int(sum_to)) / 2
        sum_ = f'{sum_from},{sum_to}'

    elif sum_from is None and sum_to is not None:
        sum_ = f'{sum_to}'

    else:
        sum_ = f'{sum_from}'

    # return round(sum_)
    return sum_


def analysis_name(name: str) -> list:
    """
    Разбирает name для выявления требуемой классификации разработчиков,
    требуемые framework.
    :param name:
    :return: Список из классификации разработчика и требуемые framework
    """
    framework = ['django', 'cherryPy', 'pyramid', 'turbogears', 'web2Py', 'flask', 'bottle', 'tornado', 'web.py',
                 'fastapi']
    developer = ['junior', 'middle', 'senior']
    developer_class = []
    required_framework = []

    strip_name = re.split(r'[,:;/ \s+]', re.sub(r'[+\-()\|]', '', name).lower())

    for el in strip_name:
        if el in developer:
            developer_class.append(el)
        elif el in framework:
            required_framework.append(el)

    return [f'{developer_class}', f'{required_framework}']


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
    ]

    db = Database()
    db.create_table(table_name, columns)
    for dict_vacancies in list_vacancies:
        db.insert_data('vacancies',dict_vacancies)

    pass


def sorting_vacancies():
    """
    тут когда-нибудь что-то будет написано по делу
    :return:
    """
    page_ = 0

    list_vacancies = []
    stop = ''

    while stop != 'stop':
        vacancies = unloading_vacancies(page_)
        time_ = random.randint(5, 30)
        # pprint.pprint(vacancies)
        print(f'страница {page_}--------------------------------------------')
        print(len(vacancies))
        print()
        if vacancies != 'stop' and len(vacancies) > 0:
            for vacancy in vacancies:
                name = vacancy.get('name')
                developer_class, required_framework = analysis_name(name)
                id_ = vacancy.get('id')
                sum_ = operations_amounts(vacancy.get('salary').get('from'), vacancy.get('salary').get('to'))
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
                    'required_framework': required_framework
                }

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
    print(len(list_vacancies))
    pprint.pprint(list_vacancies)
    return list_vacancies


if __name__ == '__main__':
    v = sorting_vacancies()
    # for r in v:
    #     print(r)
