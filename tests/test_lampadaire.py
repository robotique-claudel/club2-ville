import unittest
import sys 

sys.path.insert(0,'..')
# pylint: disable=import-error
import composant

class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 3)), 6, "Should be 6")

class TestLampadaire(unittest.TestCase):
    def test_allume(self):
        l = composant.Lampadaire(1)


if __name__ == '__main__':
    unittest.main()
