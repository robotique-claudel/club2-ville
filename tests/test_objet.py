import unittest
import sys

sys.path.insert(0, '..')
# pylint: disable=import-error
import composant  # noqa: E402


class TestObjet(unittest.TestCase):
    def test_etat_initial(self):
        o = composant.Objet(1)
        self.assertTrue(isinstance(o, composant.Objet))


class TestObjetIndependant(unittest.TestCase):
    def test_etat_initial(self):
        o = composant.ObjetIndependant(1)
        self.assertTrue(isinstance(o, composant.ObjetIndependant))

    def test_independance(self):
        o = composant.ObjetIndependant(1)
        self.assertRaises(NotImplementedError, o.controlleur)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
