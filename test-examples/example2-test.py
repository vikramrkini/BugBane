
import unittest
from example2 import multiply , divide ,negate_boolean, remove_unary_operator , replace_integer, complex_function
class TestMutants(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-4, 5), -20)
        self.assertEqual(multiply(0, 10), 0)
        
    def test_divide(self):
        self.assertEqual(divide(10, 5), 2)
        self.assertEqual(divide(-15, 3), -5)
        self.assertEqual(divide(7, 0), None)
        
    def test_negate_boolean(self):
        self.assertEqual(negate_boolean(True), False)
        self.assertEqual(negate_boolean(False), True)
        
    def test_remove_unary_operator(self):
        self.assertEqual(remove_unary_operator(5), -5)
        self.assertEqual(remove_unary_operator(-10), 10)
        
    def test_replace_integer(self):
        self.assertEqual(replace_integer(5), 6)
        self.assertEqual(replace_integer(0), 1)
        self.assertEqual(replace_integer(-5), -4)
        
    def test_complex_function(self):
        self.assertEqual(complex_function(50, 10), 120)
        self.assertEqual(complex_function(-10, 20), 20)
        self.assertEqual(complex_function(150, 5), None)
        
if __name__ == '__main__':
    unittest.main()
