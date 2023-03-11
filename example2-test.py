import unittest
from example2 import multiply, divide, negate_boolean, remove_unary_operator, replace_integer, replace_string, replace_variable, complex_function

class TestExample(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)
        self.assertIsNone(divide(6, 0))

    def test_negate_boolean(self):
        self.assertTrue(negate_boolean(False))
        self.assertFalse(negate_boolean(True))

    def test_remove_unary_operator(self):
        self.assertEqual(remove_unary_operator(5), -5)

    def test_replace_integer(self):
        self.assertEqual(replace_integer(5), 6)

    def test_replace_string(self):
        self.assertEqual(replace_string("hello"), "new string")

    def test_replace_variable(self):
        self.assertEqual(replace_variable(2, 3), 5)

    def test_complex_function(self):
        self.assertEqual(complex_function(10, 5), 30)
        self.assertEqual(complex_function(-5, 10), 10)
        self.assertIsNone(complex_function(200, 5))
