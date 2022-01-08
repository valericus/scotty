from psycopg_pool import ConnectionPool

from model import User, SearchResult


class UserDAO:
    __startup_sql = '''
    CREATE EXTENSION IF NOT EXISTS postgis;

    CREATE TABLE IF NOT EXISTS "{table_name}" (
      username VARCHAR PRIMARY KEY NOT NULL,
      location GEOGRAPHY(POINT, 4326)
    );
    '''

    __save_user_sql = '''
    INSERT INTO "{table_name}" (
      username,
      location
    ) VALUES (%s, ST_POINT(%s, %s))
    ON CONFLICT (username) DO UPDATE SET
      location = EXCLUDED.location;
    '''

    __search_sql = '''
    SELECT
      username,
      st_x(location::geometry) as x_coord,
      st_y(location::geometry) as y_coord,
      st_distance(st_point(%s, %s), location) as distance
    FROM
      "{table_name}"
    ORDER BY distance
    LIMIT %s;
    '''

    def __init__(self, connection_pool: ConnectionPool, table_name='users'):
        self._search_sql = self.__search_sql.format(table_name=table_name)
        self._save_user_sql = self.__save_user_sql.format(table_name=table_name)
        self._pool = connection_pool
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.__startup_sql.format(table_name=table_name))

    def save(self, user: User):
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self._save_user_sql, user)

    def get_nearest(self, x_coord: float, y_coord: float, count: int = 100):
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self._search_sql, (x_coord, y_coord, count))
                return [SearchResult(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
