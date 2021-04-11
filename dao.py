from math import sqrt
from sqlite3 import connect

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
    INSERT OR REPLACE INTO users (
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

    def __init__(self, path: str):
        self._path = path
        with connect(path) as connection:
            cursor = connection.cursor()
            cursor.execute(self.__startup_sql)

    def save(self, user: User):
        with connect(self._path) as connection:
            cursor = connection.cursor()
            cursor.execute(self.__save_user_sql, user)

    def get_nearest(self, x_coord: float, y_coord: float, count: int = 100):
        with connect(self._path) as connection:
            cursor = connection.cursor()
            cursor.execute(self.__search_sql, (x_coord, x_coord, y_coord, y_coord, count))
            return [SearchResult(row[0], row[1], row[2], sqrt(row[3])) for row in cursor.fetchall()]
