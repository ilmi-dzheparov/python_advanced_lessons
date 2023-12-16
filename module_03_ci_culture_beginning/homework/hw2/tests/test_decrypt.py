import unittest

from decrypt import decrypt


class TestDecryptApp(unittest.TestCase):

    def test_check_result_word(self):
        expected_result = 'абра-кадабра'
        words_for_decrypt = ['абра-кадабра.',
                             'абраа..-кадабра',
                             'абраа..-.кадабра',
                             'абра--..кадабра',
                             'абрау...-кадабра'
                             ]
        for word in words_for_decrypt:
            with self.subTest():
                self.assertEqual(decrypt(word), expected_result)

    def test_check_result_empty_string(self):
        words_for_decrypt = ['абра........', '.',]
        expected_result = ''
        for word in words_for_decrypt:
            with self.subTest():
                self.assertEqual(decrypt(word), expected_result)


    def test_check_result_symbol(self):
        words_for_decrypt = [('абр......а.', 'а'),
                             ('1..2.3', '23'),]
        for word, expected_result in words_for_decrypt:
            with self.subTest():
                self.assertEqual(decrypt(word), expected_result)