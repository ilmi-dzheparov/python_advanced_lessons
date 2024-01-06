import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_error_ignor(self):
        err_types = {ZeroDivisionError, TypeError}
        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except:
            self.fail()


    def test_error_not_ignor(self):
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'


    def test_ignor_inner_block_and_not_ignor_outer_block(self):
        outer_err_types = {TypeError}
        try:
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with self.assertRaises(TypeError):
                    with BlockErrors(inner_err_types):
                        a = 1 / '0'
        except:
            self.fail()


    def test_child_error_ignor(self):
        err_types = {Exception}
        try:
            with BlockErrors(err_types):
                a = 1 / '0'
        except:
            self.fail()




if __name__ == '__main__':
    unittest.main()
