import unittest
from example1 import calculate_fibonacci, generate_primes

class TestExample1(unittest.TestCase):
    def test_calculate_fibonacci(self):
        self.assertEqual(calculate_fibonacci(0), 0)
        self.assertEqual(calculate_fibonacci(1), 1)
        self.assertEqual(calculate_fibonacci(2), 1)
        self.assertEqual(calculate_fibonacci(3), 2)
        self.assertEqual(calculate_fibonacci(4), 3)
        self.assertEqual(calculate_fibonacci(5), 5)
        self.assertEqual(calculate_fibonacci(6), 8)

    def test_generate_primes(self):
        self.assertEqual(generate_primes(0), [])
        self.assertEqual(generate_primes(1), [])
        self.assertEqual(generate_primes(2), [2])
        self.assertEqual(generate_primes(10), [2, 3, 5, 7])
        self.assertEqual(generate_primes(20), [2, 3, 5, 7, 11, 13, 17, 19])

if __name__ == '__main__':
    unittest.main()
