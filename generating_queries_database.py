import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pprint import pprint
from database import Database
import time


def formation_filters(query_: list, dates_=None, city=None):
    """

    :param query_:
    :param dates_:
    :param city:
    :return:
    """
    framework = [
        'django', 'cherryPy', 'pyramid', 'turbogears', 'web2Py', 'flask', 'bottle',
        'tornado', 'web.py', 'fastapi'
    ]
    developer = ['junior', 'middle', 'senior']

    overall_query = []
    developer_list = []
    framework_list = []

    for el in query_:
        if el == 'python developer':
            overall_query.append(el)

        elif el in developer:
            developer_list.append(el)

        elif el in framework:
            framework_list.append(el)

    result = []

    if len(overall_query) > 0:
        header_sort_column = ''
        attachment_sort_column = ''
        result.append(db_query(header_sort_column, attachment_sort_column, dates_,
                               city, overall_query))

    if len(developer_list) > len(framework_list) and framework_list:
        header_sort_column = 'required_framework'
        attachment_sort_column = 'developer_class'
        result.append(db_query(header_sort_column, attachment_sort_column,
                               dates_, city, framework_list, developer_list))

    elif len(framework_list) > len(developer_list) and developer_list:
        header_sort_column = 'developer_class'
        attachment_sort_column = 'required_framework'
        result.append(
            db_query(header_sort_column, attachment_sort_column,
                     dates_, city, developer_list, framework_list))

    elif developer_list and framework_list and len(developer_list) == len(framework_list):
        header_sort_column = 'developer_class'
        attachment_sort_column = 'required_framework'
        result.append(
            db_query(header_sort_column, attachment_sort_column,
                     dates_, city, developer_list, framework_list))

    elif len(developer_list) > 0:
        header_sort_column = 'developer_class'
        attachment_sort_column = ''
        result.append(db_query(header_sort_column, attachment_sort_column,
                               dates_, city, developer_list))

    elif len(framework_list) > 0:
        header_sort_column = 'required_framework'
        attachment_sort_column = ''
        result.append(db_query(header_sort_column, attachment_sort_column,
                               dates_, city, framework_list))
    return result


def db_query(header_sort_column: str, attachment_sort_column: str, dates_,
             city, sort_element_header: list, sort_element_attachment: list = None, ):
    """

    :param header_sort_column:
    :param attachment_sort_column:
    :param sort_element_header:
    :param dates_:
    :param city:
    :param sort_element_attachment:
    :return:
    """
    db = Database()
    table_name = 'vacancies'
    filter_columns = ['sum']

    result = {}
    str_query = ''

    date_str = formation_filters_date() if dates_ is not None else ''
    city_str = formation_filters_city() if city is not None else ''

    for hed in sort_element_header:
        if sort_element_attachment is not None:
            for attach in sort_element_attachment:
                str_query += f"""{header_sort_column} LIKE '%{hed}%' AND
{attachment_sort_column} LIKE '%{attach}%' {date_str} {city_str}"""
                conditions = f'WHERE {str_query}'
                query_db = db.select_data(table_name, filter_columns, conditions)
                db_sum = sorted([int(val) for tup in query_db for val in tup[0].split(',')])
                if len(db_sum) > 0:
                    if hed not in result:
                        result[hed] = {}
                    result[hed][attach] = sorted(db_sum)
                str_query = ''
        else:
            if hed != 'python developer':
                str_query += f"""{header_sort_column} LIKE '%{hed}%' {date_str} {city_str}"""
                conditions = f'WHERE {str_query}'
            else:
                conditions = ''
            query_db = db.select_data(table_name, filter_columns, conditions)
            db_sum = sorted([int(val) for tup in query_db for val in tup[0].split(',')])
            if len(db_sum) > 0:
                result[hed] = sorted(db_sum)
            str_query = ''

    return result


def formation_filters_date():
    pass


def formation_filters_city():
    pass


if __name__ == '__main__':
    start = time.time()
    # query = ['python developer']
    # query = ['django', 'fastapi', 'middle']
    # query = ['django', 'junior', 'middle']
    query = ['python developer', 'django', 'fastapi', 'middle']
    # query = ['django', 'middle']
    # query = ['django', 'middle', 'senior', 'fastapi']
    # query = ['middle']
    # query = ['django']
    r = formation_filters(query)
    finish = time.time() - start
    print(r, len(r))
    print(finish)
