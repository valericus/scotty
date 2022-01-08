from collections import namedtuple

from jsonschema import validate


class User(namedtuple('User', ('username', 'x_coord', 'y_coord'))):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'x_coord': {'type': 'number'},
            'y_xoord': {'type': 'number'}
        },
        'required': ['username', 'x_coord', 'y_coord']
    }

    @classmethod
    def from_dict(cls, data: dict):
        validate(data, cls.schema)
        return cls(data['username'], data['x_coord'], data['y_coord'])


class SearchResult(namedtuple('SearchResult', ('username', 'x_coord', 'y_coord', 'distance'))):
    pass
