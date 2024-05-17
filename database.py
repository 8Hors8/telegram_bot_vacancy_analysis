import sqlite3


class Database:
    """
        тут будет док. описание
    """
    def __init__(self):
        self.con = sqlite3.connect('JobMarketDB.db')
        self.cursor = self.con.cursor()
    def create_table (self, table_name : str, columns : list):
        """
        Создает таблицу с указанным именем и строками

        :param table_name: Название таблицы
        :param columns: список столбцов
        """
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

        self.cursor.execute(create_table_query)
        self.con.commit()
