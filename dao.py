from sqlite3 import connect

from math import sqrt

from model import User, SearchResult


class UserDAO:

    __startup_sql = '''
    CREATE TABLE IF NOT EXISTS users (
      username VARCHAR(255) PRIMARY KEY,
      x_coord FLOAT,
      y_coord FLOAT
    );
    '''

    __save_user_sql = '''
    INSERT INTO users (
      username,
      x_coord,
      y_coord
    ) VALUES (?, ?, ?);
    '''

    __search_sql = '''
    SELECT
      username,
      x_coord,
      y_coord,
      (x_coord - ?) * (x_coord - ?) + (y_coord - ?) * (y_coord - ?) as square_distance
    FROM
      users
    ORDER BY square_distance
    LIMIT ?;
    '''

    @staticmethod
    def row_factory(cursor, row):
        # some dirty hack as far as SQLite doesn't support square root without some dancing
        return SearchResult(row[0], row[1], row[2], sqrt(row[3]))

    def __init__(self, path: str):
        self.db = connect(path)
        self.db.row_factory = self.row_factory
        self.cursor = self.db.cursor()

        self.cursor.execute(self.__startup_sql)
        self.cursor.connection.commit()

    def save(self, user: User):
        self.cursor.execute(self.__save_user_sql, user)
        self.cursor.connection.commit()

    def get_nearest(self, x_coord: float, y_coord: float, count: int):
        # some dirty hack as far as SQLite doesn't support square root without some dancing
        self.cursor.execute(self.__search_sql, (x_coord, x_coord, y_coord, y_coord, count))
        return self.cursor.fetchall()
