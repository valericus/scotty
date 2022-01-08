#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from configparser import ConfigParser

from psycopg_pool import ConnectionPool

from api import Api
from dao import UserDAO

parser = ArgumentParser()
parser.add_argument('--config', nargs='?', type=FileType('r'), default=open('config.ini'),
                    help='Path to config file, default is config.ini')

if __name__ == '__main__':
    args = parser.parse_args()
    config = ConfigParser()
    config.read_file(args.config)

    # TODO get pool parameters from configuration file
    connection_pool = ConnectionPool(config['database']['conninfo'])
    user_dao = UserDAO(connection_pool)
    api = Api(user_dao)
    api.app.run(config.get('http', 'host'), config.getint('http', 'port'))
