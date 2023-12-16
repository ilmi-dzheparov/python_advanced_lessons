
import unittest
from freezegun import freeze_time
import datetime

from hello_word_with_day import app




GREETINGS = (
    'Хорошего понедельника',
    'Хорошего вторника',
    'Хорошей среды',
    'Хорошего четверга',
    'Хорошей пятницы',
    'Хорошей субботы',
    'Хорошего воскресенья'
)


@freeze_time('2023-12-01')
class TestHelloWordWithDayApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_check_weekdate(self):
        username = 'ilmi' #GREETINGS[4]
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        response_text = response_text.replace(username, "")
        print(response_text)
        greeting = GREETINGS[4]
        self.assertTrue(greeting in response_text)
