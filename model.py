from collections import namedtuple

from jsonschema import validate


class User(namedtuple('User', ('username', 'lat', 'long'))):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'lat': {'type': 'number'},
            'long': {'type': 'number'}
        },
        'required': ['username', 'lat', 'long']
    }

    @classmethod
    def from_dict(cls, data: dict):
        validate(data, cls.schema)
        return cls(data['username'], data['lat'], data['long'])


class SearchResult(namedtuple('SearchResult', ('username', 'lat', 'long', 'distance'))):
    pass
