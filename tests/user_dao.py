import logging

from dao import UserDAO
from model import SearchResult, User

_log = logging.getLogger(__name__)


def test_save_and_get(connection_pool, test_table_name):
    _log.info(f'Started test with table name {test_table_name}')
    dao = UserDAO(connection_pool, test_table_name)
    dao.save(User('Pavel Andreievich Chekov', 15, 21))
    expected_result = [SearchResult('Pavel Andreievich Chekov', 15, 21, 4)]

    actual_result = dao.get_nearest(15, 25)

    assert actual_result == expected_result


def test_sorting(connection_pool, test_table_name):
    _log.info(f'Started test with table name {test_table_name}')
    dao = UserDAO(connection_pool, test_table_name)
    dao.save(User('Leonard McCoy', 3, 2))
    dao.save(User('James Tiberius Kirk', 2, 3))
    dao.save(User('Spock', 13, 25))

    actual_result = dao.get_nearest(5, 8)

    assert \
        [i.username for i in actual_result] == \
        ['James Tiberius Kirk', 'Leonard McCoy', 'Spock']


def test_replace(connection_pool, test_table_name):
    _log.info(f'Started test with table name {test_table_name}')
    dao = UserDAO(connection_pool, test_table_name)
    dao.save(User('Pavel Andreievich Chekov', 15, 21))
    dao.save(User('Pavel Andreievich Chekov', 1, 1))
    expected_result = [SearchResult('Pavel Andreievich Chekov', 1, 1, 5)]

    actual_result = dao.get_nearest(4, 5)

    assert actual_result == expected_result
