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

class Objet:
    def __init__(self, *args, **kwargs):
        pass
    
    def commence(self):
        self.controlleur()

    def controlleur(self):
        raise NotImplementedError


class Lampadaire(Objet):
    def __init__(self, id, *args, **kwargs):
        self.id = id
        super().__init__(self, *args, **kwargs)

    def allume(self):
        self.est_allume = True
        log.debug("Lampadaire est allume")
        
    def eteind(self):
        self.est_allume = False
        log.debug("Lampadaire est eteind")
        
    def controlleur(self):        
        while True:
            num = randint(1, 10)
            if num == 1:
                self.eteind()
            elif num == 10:
                self.allume()
            sleep(0.1)

class FeuCirculation(Objet):
    def __init__(self, *args, **kwargs):
        # setup... 
        super().__init__(self, *args, **kwargs)
    
    

