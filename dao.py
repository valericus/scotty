from typing import Iterable

from psycopg_pool import ConnectionPool

from model import User, SearchResult


class UserDAO:
    __startup_sql = '''
    create extension if not exists postgis;

    create table if not exists "{table_name}" (
      username varchar primary key not null,
      location geography(point, 4326)
    );
    '''

    __save_user_sql = '''
    insert into "{table_name}" (
      username,
      location
    ) values (%s, st_point(%s, %s))
    on conflict (username) do update set
      location = excluded.location;
    '''

    __search_sql = '''
    select
      username,
      st_x(location::geometry) as lat,
      st_y(location::geometry) as long,
      st_distance(st_point(%s, %s), location) as distance
    from
      "{table_name}"
    order by distance
    limit %s;
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

    def save_many(self, users: Iterable[User]):
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(self._save_user_sql, users)

    def get_nearest(self, lat: float, long: float, count: int = 100):
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self._search_sql, (lat, long, count))
                return [SearchResult(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
