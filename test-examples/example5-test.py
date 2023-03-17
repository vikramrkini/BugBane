import unittest
from example5 import haversine

class TestHaversine(unittest.TestCase):
    def test_same_coordinate(self):
        self.assertEqual(haversine(0, 0, 0, 0), 0)

    def test_different_latitude(self):
        self.assertAlmostEqual(haversine(0, 0, 1, 0), 111.195, delta=0.1)

    def test_different_longitude(self):
        self.assertAlmostEqual(haversine(0, 0, 0, 1), 111.195, delta=0.1)

    def test_different_coordinates(self):
        self.assertAlmostEqual(haversine(40, -75, 37.7749, -122.4194), 4133.05, delta=10)

if __name__ == '__main__':
    unittest.main()
