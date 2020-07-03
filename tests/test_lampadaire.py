import unittest
import sys

sys.path.insert(0, '..')
# pylint: disable=import-error
import composant  # noqa: E402


class TestLampadaire(unittest.TestCase):
    def test_allume(self):
        L = composant.Lampadaire(1, 11)
        self.assertTrue(isinstance(L, composant.Lampadaire))


if __name__ == '__main__':
    unittest.main()
