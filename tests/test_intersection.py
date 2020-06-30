import unittest
import sys 
from time import sleep

sys.path.insert(0,'..')
# pylint: disable=import-error
from composant import FeuCirculation, Intersection


class TestIntersection(unittest.TestCase):
    def test_fonctionne(self):
        n = FeuCirculation(1)
        s = FeuCirculation(2)
        e = FeuCirculation(3)
        o = FeuCirculation(4)
        i = Intersection(1, n, e, s, o)
        self.assertTrue(isinstance(i, Intersection))
    
    def test_etat_initial(self):
        n = FeuCirculation(1)
        s = FeuCirculation(2)
        e = FeuCirculation(3)
        o = FeuCirculation(4)
        Intersection(1, n, e, s, o)
        self.assertEqual(n.etat, 3)
        self.assertEqual(s.etat, 3)
        self.assertEqual(e.etat, 1)
        self.assertEqual(o.etat, 1)
    
    def test_changement_axe(self):
        n = FeuCirculation(1)
        s = FeuCirculation(2)
        e = FeuCirculation(3)
        o = FeuCirculation(4)
        i = Intersection(1, n, e, s, o)
        i.changeAxe()
        sleep(0.1) # important
        self.assertEqual(n.etat, 1)
        self.assertEqual(s.etat, 1)
        self.assertEqual(e.etat, 3)
        self.assertEqual(o.etat, 3)




if __name__ == '__main__':
    unittest.main()
