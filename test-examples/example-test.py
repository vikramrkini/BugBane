import unittest
import example

class TestExample(unittest.TestCase):
    def test_add(self):
        self.assertEqual(example.add(2, 3), 5)
    
    def test_multiply(self):
        self.assertEqual(example.multiply(2, 3), 6)
    
    def test_is_even(self):
        self.assertTrue(example.is_even(2))
        self.assertFalse(example.is_even(3))
