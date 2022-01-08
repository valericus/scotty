from uuid import uuid4

import pytest
from psycopg_pool import ConnectionPool


def pytest_addoption(parser):
    parser.addoption(
        "--conninfo", action="store", help="Postgres connection string"
    )


@pytest.fixture
def connection_pool(request):
    return ConnectionPool(request.config.getoption("--conninfo"))


@pytest.fixture
def test_table_name(connection_pool):
    table_name = f'test_table_{uuid4()}'
    yield table_name
    with connection_pool.getconn() as connection:
        connection.execute(f'DROP TABLE "{table_name}"')
