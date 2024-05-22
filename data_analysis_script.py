import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pprint import pprint
from database import Database


def database_query(query_: list):
    """

    :param query_:
    :return:
    """
    framework = ['django', 'cherryPy', 'pyramid', 'turbogears', 'web2Py', 'flask', 'bottle',
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

    table_name = 'vacancies'
    result = {}
    db = Database()

    if len(overall_query) > 0:
        filter_columns = ['sum']
        full_db = db.select_data(table_name, filter_columns)
        ful = [int(val) for tup in full_db for val in tup[0].split(',')]
        result['python_developer'] = sorted(ful)

    developer_query = ''
    framework_query = ''

    if len(developer_list) > len(framework_list):

        for el in developer_list:

            if len(framework_list) > 0:
                for com in framework_list:
                    developer_query = ''
                    framework_query = ''

                    if len(developer_query) > 0:
                        developer_query += ' OR '
                    developer_query += f"""developer_class like'%{el}%'"""

                    if len(framework_query) > 0:
                        framework_query += ' OR '
                    framework_query += f"""required_framework like'%{com}%'"""

                    filter_columns = ['sum']
                    query_str = f"""{developer_query} AND {framework_query}"""
                    conditions = f'WHERE {query_str}'

                    developer_db = db.select_data(table_name, filter_columns, conditions)
                    developer_sum = [int(val) for tup in developer_db for val in tup[0].split(',')]

                    if len(developer_sum) > 0:
                        if com not in result:
                            result[com] = {}
                        result[com][el] = sorted(developer_sum)
            else:
                if len(developer_query) > 0:
                    developer_query += ' OR '
                developer_query += f"""developer_class like'%{el}%'"""

                filter_columns = ['sum']
                query_str = f"""{developer_query}"""
                conditions = f'WHERE {query_str}'

                developer_db = db.select_data(table_name, filter_columns, conditions)
                developer_sum = [int(val) for tup in developer_db for val in tup[0].split(',')]

                if len(developer_sum) > 0:
                    result[el] = sorted(developer_sum)
                developer_query = ''

    elif len(developer_list) < len(framework_list):
        for el in framework_list:
            if len(developer_list) > 0:
                for com in developer_list:
                    developer_query = ''
                    framework_query = ''
                    if len(developer_query) > 0:
                        developer_query += ' OR '
                    developer_query += f"""developer_class like'%{com}%'"""

                    if len(framework_query) > 0:
                        framework_query += ' OR '
                    framework_query += f"""required_framework like'%{el}%'"""

                    filter_columns = ['sum']
                    query_str = f"""{framework_query} AND {developer_query}"""
                    conditions = f'WHERE {query_str}'

                    developer_db = db.select_data(table_name, filter_columns, conditions)
                    developer_sum = [int(val) for tup in developer_db for val in tup[0].split(',')]

                    if len(developer_sum) > 0:
                        if com not in result:
                            result[com] = {}
                        result[com][el] = sorted(developer_sum)
            else:
                if len(framework_query) > 0:
                    framework_query += ' OR '
                framework_query += f"""required_framework like'%{el}%'"""

                filter_columns = ['sum']
                query_str = f"""{framework_query}"""
                conditions = f'WHERE {query_str}'

                developer_db = db.select_data(table_name, filter_columns, conditions)
                developer_sum = [int(val) for tup in developer_db for val in tup[0].split(',')]

                if len(developer_sum) > 0:
                    result[el] = sorted(developer_sum)
                framework_query = ''
    return result



if __name__ == '__main__':
    query = ['django', 'fastapi','middle']
    r = database_query(query)
    print(r)
