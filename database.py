import sqlite3


class Database:
    """
        тут будет док. описание
    """

    def __init__(self):
        self.con = sqlite3.connect('JobMarketDB.db')
        self.cursor = self.con.cursor()

    def create_table(self, table_name: str, columns: list):
        """
        Создает таблицу с указанным именем и строками

        :param table_name: Название таблицы
        :param columns: список столбцов
        """
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

        self.cursor.execute(create_table_query)
        self.con.commit()

    def insert_data(self, table_name: str, data: dict):
        """
        Вносит дынные в таблицу с именем table_name

        :param table_name:Название таблицы
        :param data:список данных для внесения
        """


        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])

        insert_query = f"""
            INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
            """

        values = list(data.values())

        self.cursor.execute(insert_query, values)
        self.con.commit()

    def select_data(self, table_name, conditions):
        """
        Выгрузка данных с базы данных
        :param table_name:Название таблицы
        :param conditions:
        """
        pass

    def close_connection(self):
        """
        Закрывает соединение с базой данных
        """
        self.con.close()
