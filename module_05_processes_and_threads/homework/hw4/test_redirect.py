import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def test_stream_is_in_file(self):
        test_stdout = open('test_stdout.txt', 'w')
        test_stderr = open('test_stderr.txt', 'w')
        with Redirect(stdout=test_stdout, stderr=test_stderr):
            print('Hello stdout.txt')
            raise Exception('Hello stderr.txt')

        with open('test_stdout.txt', 'r') as t1:
            with open('test_stderr.txt', 'r') as t2:
                content_stdout = t1.read()
                content_stderr = t2.read()
                self.assertIn('Hello stdout.txt', content_stdout)
                self.assertIn('Hello stderr.txt', content_stderr)


if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
