from database import Database

framework = ['django', 'cherryPy', 'pyramid', 'turbogears', 'web2Py', 'flask', 'bottle',
             'tornado', 'web.py', 'fastapi'
             ]
developer = ['junior', 'middle', 'senior']

language = ['python']


def city():
    """
    Получает уникальные названия городов из базы данных vacancies и возвращает список городов.
    :return:Список уникальных названий городов.
    """
    if not hasattr(city, 'call_count'):
        city.call_count = 0
    cities = []
    if not cities or city.call_count % 10 == 0:
        bd = Database()
        data = bd.select_data('vacancies', ['DISTINCT area'])
        for item in data:
            city_data_str = item[0].strip("()").replace("'", "").replace("[", "").replace("]", "")
            city_name = city_data_str.split(", ")[1].strip()
            cities.append(city_name)
    city.call_count += 1
    return cities


if __name__ == '__main__':
    pass
