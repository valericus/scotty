from collections import namedtuple

from jsonschema import validate


class User(namedtuple('User', ('username', 'x_coord', 'y_coord'))):
    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'x_coord': {'type': 'number'},
            'y_xoord': {'type': 'number'}
        }
    }

    @classmethod
    def from_dict(cls, data: dict):
        validate(data, cls.schema)
        return cls(data['username'], data['x_coord'], data['y_coord'])

    def to_dict(self):
        return {
            'username': self.username,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord
        }


class SearchResult(namedtuple('SearchResult', ('username', 'x_coord', 'y_coord', 'distance'))):

    def to_dict(self):
        return {
            'username': self.username,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'distance': self.distance
        }
