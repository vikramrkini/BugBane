import unittest
from program import check_numbers

class TestCheckNumbers(unittest.TestCase):
    def test_largest_number(self):
        self.assertEqual(check_numbers(10, 20, 30), "30 is the largest number.")
        self.assertEqual(check_numbers(3, 5, 2), "5 is the largest number.")
        
    def test_all_numbers_equal(self):
        self.assertEqual(check_numbers(10, 10, 10), "All numbers are equal.")
        
    def test_none_largest_number(self):
        self.assertEqual(check_numbers(7, 4, 4), "None of the numbers is the largest.")
        
if __name__ == '__main__':
    unittest.main()
