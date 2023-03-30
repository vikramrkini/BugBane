import sys

import unittest
from example4 import add_numbers, subtract_numbers,multiply_numbers,divide_numbers,is_even,is_odd, compare_numbers, remove_unary_operator,replace_string,replace_variable,replace_integer,negate_boolean,invert_negatives

class TestMathFunctions(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-2, 3), 1)
        
    def test_subtract_numbers(self):
        self.assertEqual(subtract_numbers(5, 2), 3)
        self.assertEqual(subtract_numbers(2, 5), -3)
        
    def test_multiply_numbers(self):
        self.assertEqual(multiply_numbers(2, 3), 6)
        self.assertEqual(multiply_numbers(-2, 3), -6)
        
    def test_divide_numbers(self):
        self.assertEqual(divide_numbers(6, 3), 2)
        self.assertEqual(divide_numbers(3, 1), 3)
        
    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(3))
        
    def test_is_odd(self):
        self.assertTrue(is_odd(3))
        self.assertFalse(is_odd(2))
        
    def test_compare_numbers(self):
        self.assertTrue(compare_numbers(2, 2))
        self.assertFalse(compare_numbers(2, 3))
        
    def test_negate_boolean(self):
        self.assertTrue(negate_boolean(False))
        self.assertFalse(negate_boolean(True))
        
    def test_remove_unary_operator(self):
        self.assertEqual(remove_unary_operator(5), -5)
        self.assertEqual(remove_unary_operator(-5), 5)
        
    def test_replace_integer(self):
        self.assertEqual(replace_integer(5), 47)
        self.assertEqual(replace_integer(-5), 37)
        
    def test_replace_string(self):
        self.assertEqual(replace_string('hello world'), 'world world')
        self.assertEqual(replace_string('goodbye world'), 'goodbye world')
        
    def test_replace_variable(self):
        self.assertEqual(replace_variable(5), 6)
        self.assertEqual(replace_variable(-5), -4)
        
    def test_invert_negatives(self):
        self.assertEqual(invert_negatives(5), -5)
        self.assertEqual(invert_negatives(-5), 5)

if __name__ == '__main__':
    unittest.main()
