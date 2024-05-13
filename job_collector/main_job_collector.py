import random

import requests
from time import sleep


def unloading_vacancies(page_):
    url = 'https://api.hh.ru/vacancies'

    params = {'text': '!"python developer" NOT C++',
              'area': 1,
              'per_page': 100,
              'page': page_,
              'only_with_salary': 'true'
              }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get('items', [])
        return vacancies
    else:
        print('Ошибка при запросе данных:', response.status_code)
        return 'stop'


page_ = 0

list_vacancies = []
stop = ''

while stop != 'stop':
    vacancies = unloading_vacancies(page_)
    time_ = random.randint(5, 30)
    print(f'страница {page_}--------------------------------------------')
    print(len(vacancies))
    print()
    if vacancies != 'stop' and len(vacancies) > 0:
        for vacancy in vacancies:
            # print(vacancy.get('name'))
            # print(vacancy.get('employer', {}).get('name'))
            # print(vacancy.get('snippet').get('requirement'))

            name = vacancy.get('name')
            try:
                sum_ = f"от {vacancy.get('salary').get('from')} до {vacancy.get('salary').get('to')} {vacancy.get('salary').get('currency')}"
                # print(
                #     f"4 от {vacancy.get('salary').get('from')} до {vacancy.get('salary').get('to')} {vacancy.get('salary').get('currency')}")
                str_vacancy = f'{name} суммы {sum_}'
                list_vacancies.append(str_vacancy)
                print(vacancy.get("name"), '-', vacancy.get("id"))
            except AttributeError:
                pass
                # print('нет суммы')
            # print('---')
    elif len(vacancies) == 0:
        break
    else:
        stop = vacancies
    page_ += 1
    sleep(time_)

print(len(list_vacancies))
print(list_vacancies)
