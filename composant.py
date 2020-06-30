"""
Fichier contenants les objets
"""
import json
import logging
import logging.config
import os
from random import randint
from time import sleep
import threading


log = logging.getLogger(__name__)

os.system("clear")

type_objet_connecte = []
objets = []

class Objet:
    def __init__(self, ids, *args, **kwargs):
        self.ids = ids
        log.info("Nouveau objet %s", type(self))
        type_objet_connecte.append(type(self))
        objets.append(self)
        pass

    # def __str__(self):
    #     return f"{type(self)}-{self.id}"
    
class ObjetIndependant(Objet):
    def __init__(self, ids, *args, **kwargs):
        super().__init__(self, ids, *args, **kwargs)

    def commence(self):
        x = threading.Thread(target=self.controlleur) #, daemon=True)
        x.start()

    def controlleur(self):
        raise NotImplementedError
    

class Lampadaire(ObjetIndependant):
    def __init__(self, ids, *args, **kwargs):
        self.id = ids
        self.est_allume = False
        super().__init__(self, ids, *args, **kwargs)

    def allume(self):
        self.est_allume = True
        log.debug("Lampadaire est allume")
        
    def eteind(self):
        self.est_allume = False
        log.debug("Lampadaire est eteind")
        
    def controlleur(self):   
        log.debug("Controlleur a debute")     
        while True:
            num = randint(1, 10) 
            if num == 1:
                self.eteind()
            elif num == 10:
                self.allume()
            sleep(0.1)


class FeuCirculation(Objet):
    def __init__(self, ids, *args, **kwargs):
        self.etat = 3  # 1: vert, 2: orange, 3: rouge
        self.temps_orange = 3  # temps a passer sur l'orage
        self.ids = ids
        super().__init__(self, ids, *args, **kwargs)
    
    def vert(self):
        self.etat = 1
    
    def rouge(self):
        x = threading.Thread(target=self._rougeOrange) #, daemon=True)
        if self.etat == 1:
            x.start()
    
    def _rougeOrange(self):
        self.etat = 2
        sleep(self.temps_orange)
        self.etat = 3


class Intersection(Objet):
    def __init__(self, ids, nord, est, sud, ouest, *args, **kwargs):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest
        self.axes = [[nord, sud], [est, ouest]]
        self.ids = ids
       

        for i in self.axes[0]:
            i.rouge()
        for i in self.axes[1]:
            i.vert()
        super().__init__(self, id, *args, **kwargs)

    def changeAxe(self):
        if (self.axes[0][0].etat == 1):
            for i in self.axes[0]:
                i.rouge()
            sleep(3)
            for i in self.axes[1]:
                i.vert()
        else:
            for i in self.axes[1]:
                i.rouge()
            sleep(3)
            for i in self.axes[0]:
                i.vert()
    
    
    
    

