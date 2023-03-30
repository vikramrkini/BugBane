import unittest
from example3 import find_largest
class TestFindLargest(unittest.TestCase):
    def test_find_largest_basic(self):
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(find_largest(numbers), 5)

    def test_find_largest_negative_numbers(self):
        numbers = [-5, -2, -1, -10, -7]
        self.assertEqual(find_largest(numbers), -1)

    def test_find_largest_duplicate_numbers(self):
        numbers = [10, 10, 5, 8, 9]
        self.assertEqual(find_largest(numbers), 10)

    def test_find_largest_single_number(self):
        numbers = [3]
        self.assertEqual(find_largest(numbers), 3)

    def test_find_largest_empty_list(self):
        numbers = []
        with self.assertRaises(IndexError):
            find_largest(numbers)

if __name__ == '__main__':
    unittest.main()
