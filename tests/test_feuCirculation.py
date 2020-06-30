import unittest
import sys 

sys.path.insert(0,'..')
# pylint: disable=import-error
from composant import FeuCirculation, Intersection


class TestIntersection(unittest.TestCase):
    def test_fonctionne(self):
        f = FeuCirculation(1)
        self.assertTrue(isinstance(f, FeuCirculation))
    
    def test_etat_initial(self):
        f = FeuCirculation(1)
        self.assertEqual(f.etat, 3)
    
    def test_rouge(self):
        f = FeuCirculation(1)
        f.rouge()
        self.assertEqual(f.etat, 3)
    
    def test_vert(self):
        f = FeuCirculation(1)
        f.vert()
        self.assertEqual(f.etat, 1)

    

if __name__ == '__main__':
    unittest.main()
