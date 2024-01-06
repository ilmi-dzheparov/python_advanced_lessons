import json
import unittest
from remote_execution import app


class TestRemoteExecution(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()


    def test_check_timeout_is_less_then_time_of_operation(self):
        data = {'code': 'print(99 ** 9999999999999999999999)', 'timeout': 1}
        response = self.app.post('/run_code', json=data, content_type='application/json')
        result = json.loads(response.data)
        expected_result = {'stdout': '', 'stderr': 'Timeout is expired'}
        self.assertEqual(result, expected_result)


    def test_incorrect_input_data_code(self):
        data = {'code': None, 'timeout': 1}
        response = self.app.post('/run_code', json=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertIn('This field is required.', result['error'])


    def test_incorrect_input_data_timeout(self):
        data = {'code': 'print("something")', 'timeout': "a"}
        response = self.app.post('/run_code', json=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertIn('Not a valid integer value.', result['error'])


    def test_not_safe_input_data_code(self):
        data = {'code': 'print()"; echo "hacked', 'timeout': 10}
        response = self.app.post('/run_code', json=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertIn('hacked', result['stdout'])


if __name__ == '__main__':
    unittest.main()
