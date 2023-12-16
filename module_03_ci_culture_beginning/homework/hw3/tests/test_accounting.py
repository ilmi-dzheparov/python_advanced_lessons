import unittest
from unittest.mock import patch

from accounting import app

storage = {
    1991: {
        10: {
            12: 200,
            13: 100,
            'total': 300,
        },
        11: {
            6: 400,
            8: 330,
            'total': 730,
        },
        'total': 1030,
    },
    1992: {
        8: {
            8: 400,
            16: 250,
            'total': 650,
        },
        9: {
            3: 200,
            4: 230,
            'total': 430,
        },
        'total': 1080,
    },
}
storage_empty = {}


class TestAccountingApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.base_url_1 = '/add/'
        self.base_url_2 = '/calculate/'
        self.app = app.test_client()
        self.storage = {
            1991: {
                10: {
                    12: 200,
                    13: 100,
                    'total': 300,
                },
                11: {
                    6: 400,
                    8: 330,
                    'total': 730,
                },
                'total': 1030,
            },
            1992: {
                8: {
                    8: 400,
                    16: 250,
                    'total': 650,
                },
                9: {
                    3: 200,
                    4: 230,
                    'total': 430,
                },
                'total': 1080,
            },
        }

    def test_add_status_code_200(self):
        """
        Test status code 200
        :return:
        """
        response = self.app.get(self.base_url_1 + '19911020/300')
        self.assertEqual(200, response.status_code)

    def test_add_date_value_error(self):
        """
        Test raising value error
        :return:
        """
        with self.assertRaises(ValueError):
            self.app.get(self.base_url_1 + 'asgdfdbas/300')

    def test_add_finance_status_code_404(self):
        """
        Test incorrect data in query string (expense)
        Test status code 404
        :return:
        """
        response = self.app.get(self.base_url_1 + '19911020/300u')
        self.assertEqual(404, response.status_code)

    @patch('accounting.storage', storage)
    def test_calculate_year_result(self):
        """
        Test calculate of year is working
        :return:
        """
        age = 1991
        response = self.app.get(self.base_url_2 + str(age))
        response_text = response.data.decode()

        total_1 = self.storage[age]['total']
        self.assertTrue(str(total_1) in response_text)

    @patch('accounting.storage', storage)
    def test_calculate_year_status_code_404(self):
        """
        Test incorrect data in query string (year)
        :return:
        """
        response = self.app.get(self.base_url_1 + '199')
        self.assertEqual(404, response.status_code)

    @patch('accounting.storage', storage_empty)
    def test_calculate_year_empty_is_working(self):
        """
        Test empty storage calculating year
        :return:
        """
        age = 1991
        response = self.app.get(self.base_url_2 + str(age))
        response_text = response.data.decode()
        self.assertIn('0', response_text)

    @patch('accounting.storage', storage)
    def test_calculate_month_result(self):
        """
        Test calculate of month is working
        :return:
        """
        age = 1991
        month = 10
        response = self.app.get(self.base_url_2 + str(age) +'/' + str(month))
        response_text = response.data.decode()

        total_1 = self.storage[age][month]['total']
        self.assertTrue(str(total_1) in response_text)

    @patch('accounting.storage', storage)
    def test_calculate_month_status_code_404(self):
        """
        Test incorrect data in query string (month)
        :return:
        """
        response = self.app.get(self.base_url_1 + '1991' + '/' + '13u')
        self.assertEqual(404, response.status_code)

    @patch('accounting.storage', storage_empty)
    def test_calculate_month_empty_is_working(self):
        """
        Test empty storage calculating month
        :return:
        """
        age = 1991
        month = 1
        response = self.app.get(self.base_url_2 + str(age) +'/' + str(month))
        response_text = response.data.decode()
        self.assertIn('0', response_text)
