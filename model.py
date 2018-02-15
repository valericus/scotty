from collections import namedtuple
from math import sqrt

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

    @classmethod
    def for_user(cls, user: User, x_coord: float, y_coord: float):
        distance = sqrt((user.x_coord - x_coord) ** 2 + (user.y_coord - y_coord) ** 2)
        return cls(user.username, user.x_coord, user.y_coord, distance)

    def to_dict(self):
        return {
            'username': self.username,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'distance': self.distance
        }
