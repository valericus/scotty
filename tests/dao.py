from os import remove, close
from tempfile import mkstemp
from unittest import TestCase

from dao import UserDAO
from model import SearchResult, User


class UserDAOTestCase(TestCase):

    def setUp(self):
        fd, self.db_path = mkstemp()
        close(fd)
        self.dao = UserDAO(self.db_path)

    def tearDown(self):
        del self.dao
        remove(self.db_path)

    def test_save_and_get(self):
        self.dao.save(User('Pavel Andreievich Chekov', 15, 21))
        expected_result = [SearchResult('Pavel Andreievich Chekov', 15, 21, 4)]

        actual_result = self.dao.get_nearest(15, 25)

        self.assertEqual(actual_result, expected_result)

    def test_sorting(self):
        self.dao.save(User('Leonard McCoy', 3, 2))
        self.dao.save(User('James Tiberius Kirk', 2, 3))
        self.dao.save(User('Spock', 13, 25))

        actual_result = self.dao.get_nearest(5, 8)

        self.assertEqual(
            [i.username for i in actual_result],
            ['James Tiberius Kirk', 'Leonard McCoy', 'Spock']
        )

    def test_replace(self):
        self.dao.save(User('Pavel Andreievich Chekov', 15, 21))
        self.dao.save(User('Pavel Andreievich Chekov', 1, 1))
        expected_result = [SearchResult('Pavel Andreievich Chekov', 1, 1, 5)]

        actual_result = self.dao.get_nearest(4, 5)

        self.assertEqual(actual_result, expected_result)