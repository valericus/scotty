from unittest import TestCase

from jsonschema import ValidationError

from model import User


class UserTestCase(TestCase):

    def test_from_dict(self):
        input = {
            'username': 'Montgomery Christopher Jorgensen Scott',
            'x_coord': 23,
            'y_coord': 32
        }
        expected_result = User('Montgomery Christopher Jorgensen Scott', 23, 32)
        self.assertEqual(User.from_dict(input), expected_result)

    def test_from_dist_with_bad_data(self):
        no_username = {
            'x_coord': 23,
            'y_coord': 32
        }
        no_x_coord = {
            'username': 'Montgomery Christopher Jorgensen Scott',
            'y_coord': 32
        }
        no_y_coord = {
            'username': 'Montgomery Christopher Jorgensen Scott',
            'x_coord': 23
        }
        non_number_coords = {
            'username': 'Montgomery Christopher Jorgensen Scott',
            'x_coord': '23',
            'y_coord': '32'
        }

        for data in (no_username, no_x_coord, no_y_coord, non_number_coords):
            with self.assertRaises(ValidationError):
                User.from_dict(data)
