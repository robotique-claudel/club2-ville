import unittest
import sys 

sys.path.insert(0,'..')
# pylint: disable=import-error
import composant

class TestLampadaire(unittest.TestCase):
    def test_allume(self):
        l = composant.Lampadaire(1)
        self.assertTrue(isinstance(l, composant.Lampadaire))


if __name__ == '__main__':
    unittest.main()
