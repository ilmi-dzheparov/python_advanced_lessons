"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
import json
import unittest

from hw1_registration import app

# data = {
#     "email": "bob@gmail.com",
#     "phone": 9039999999,
#     "name": "bob",
#     "address": "new_address",
#     "index": 123456,
# }

class TestRegistrationValidators(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.base_url = '/registration'
        self.app = app.test_client()
        self.data = {
            "email": "bob@gmail.com",
            "phone": 9039999999,
            "name": "bob",
            "address": "new_address",
            "index": 123456,
        }

    def tearDown(self):
        ...

    def test_all_validators_are_correct(self):
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_email_is_incorrect(self):
        self.data["email"] = "bobgmail.com"
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_phone_is_incorrect(self):
        self.data["phone"] = 901999999
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_name_is_incorrect(self):
        self.data["name"] = None
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_address_is_incorrect(self):
        self.data["address"] = None
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_index_is_incorrect(self):
        self.data["index"] = "index"
        response = self.app.post(self.base_url, json=self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)



if __name__ == '__main__':
    unittest.main()
