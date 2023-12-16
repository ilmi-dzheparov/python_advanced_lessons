import datetime
import unittest
from person import Person

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.name = 'Anton'
        self.yob = 1983
        self.address = "adress"
        self.person = Person(self.name, self.yob, self.address)

    def tearDown(self):
        print("Тест завершен.")

    def test_get_age_is_working(self):
        age = datetime.datetime.now().year - self.yob
        age_ = self.person.get_age()
        self.assertEqual(age, age_)

    def test_get_name_is_working(self):
        name_ = self.person.get_name()
        self.assertEqual(self.name, name_)

    def test_set_name_is_working(self):
        name = "Ivan"
        self.person.set_name(name)
        name_ = self.person.name
        self.assertEqual(name, name_)

    def test_set_address_is_working(self):
        address = "Another address"
        self.person.set_address(address)
        address_ = self.person.address
        self.assertEqual(address, address_)

    def test_get_address_is_working(self):
        address_ = self.person.get_address()
        self.assertEqual(self.address, address_)

    def test_is_homeless_is_working(self):
        self.person.set_address(None)
        response = self.person.is_homeless()
        self.assertEqual(response, True)
