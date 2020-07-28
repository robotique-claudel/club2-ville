""" @package composant
"""
from datetime import datetime
import json
import logging
import logging.config
import os
from random import randint
import requests
from time import sleep
import threading

from influxdb import InfluxDBClient


log = logging.getLogger(__name__)

os.system("clear")

type_objet_connecte = []
objets = []

ARDUINO_URL = "http://192.168.1.105"

client = InfluxDBClient(host='influxdb', port=8086)


class Objet:
    """
    La classe de base pour un objet.

    Cette classe est une classe abstraite qui ne devrait
    pas être créé manuellement
    """
    def __init__(self, ids, *args, **kwargs):
        """
        Crée un nouveau Objet

    Cette fonction initialise l'objet et l'ajoute a une
    liste de tous les objets. Cette fonction devrait être
    appelé par une classe descendante.

        Args:
            ids:     Un id unique pour identifier l'objet
            args:   Des arguments supplémentaires

        Kwargs:
            kwargs:  Des arguments supplémentaires sous la forme `foo=bar`

        Returns:
            None
        """
        log.info("Nouveau objet %s", ids)
        type_objet_connecte.append(type(self))
        objets.append(self)

    def commande(self, pinstr, comstr, setto=None):
        uri = ""
        if setto is not None:
            uri = f"/{pinstr}/{comstr}/{setto}"
        else:
            uri = f"/{pinstr}/{comstr}"
        url = ARDUINO_URL + uri
        log.debug("Envoie de la commande: %s", url)
        res = requests.get(url)

        strres = res.content
        strres = strres.decode('UTF-8')
        strres = strres.replace('\n',  '')
        strres = strres.replace('\r', '')

        obj = json.loads(strres)
        return obj

    def __str__(self):
        return f"{type(self)}-{self.ids}"


class ObjetIndependant(Objet):
    """
    Une classe qui représente un objet qui peut agir de facon indépendante

    Cette classe est une classe abstraite qui ne devrait
    pas être créé manuellement
    """
    def __init__(self, ids, *args, **kwargs):
        """
        Crée un nouveau ObjetIndependant

        Cette fonction initialise un nouveau ObjetIndependant
        mais ne débute pas sa fonction controlleur

        Args:
            ids:     Un id unique pour identifier l'objet
            args:   Des arguments supplémentaires

        Kwargs:
            kwargs:  Des arguments supplémentaires sous la forme `foo=bar`

        Returns:
            None
        """
        self.ids = ids
        # pylint: disable=no-member
        super().__init__(self.ids, *args, **kwargs)

    def commence(self):
        """
        Débute la fonction controlleur de l'ObjetIndependant

        Afin que la fonction controlleur puisse agir de façon indépendante,
        la fonction est débuté sur une thread séparé.

        Returns:
            None

        Raises:
            NotImplementedError
        """
        x = threading.Thread(target=self.controlleur)
        x.start()

    def controlleur(self):
        """
        La fonction qui controlle l'ObjetIndependant

        Cette fonction doit être implimenté par une classe descendante,
        et constitue normallement d'une boucle infinie contenant le code
        de l'objet

        Raises:
            NotImplementedError


        Examples:
            >>> ObjetIndependant(1).controlleur()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError


class Senseur(ObjetIndependant):
    """
    Une classe qui représente un capteur/senseur

    Cette classe doit s'occuper de la collection de l'information
    ainsi que son reportage
    Cette classe est une classe abstraite qui ne devrait
    pas être créé manuellement

    Returns:
        None
    """
    def __init__(self, ids, pin, intervalle, measurement, *args, **kwargs):
        """
        Crée un nouveau Senseur

        Cette fonction initialise un nouveau Senseur

        Args:
            ids:          Un id unique pour identifier l'objet
            pin:          Le pin sur lequel le capteur est attaché sur
                          le microcontrolleur
            intervalle:   L'intervalle entre la collecte de l'information
                           en secondes
            measurement:  Le nom de ce qui est mesuré telle qu'il doit
                          apparaitre dans la base de donné
            args:         Des arguments supplémentaires

        Kwargs:
            kwargs:  Des arguments supplémentaires sous la forme `foo=bar`

        Returns:
            None
        """
        self.ids = ids
        self.pin = pin
        self.intervalle = intervalle
        self.measurement = measurement
        # pylint: disable=no-member
        super().__init__(self.ids, *args, **kwargs)

    def collection(self):
        """
        Controlle la facon dont l'information est collecté

        Cette fonction controlle la collection de l'information
        du capteur mais aussi la facon dont l'information doit etre
        reporte. Cette fonction doit etre implimente par une classe
        descendante

        Returns:
            None

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def controlleur(self):
        """
        Le controlleur du capteur

        Cette fonction est le controlleur du capteur. Elle commence
        la collection, puis attends pour intervalle secondes dans une
        boucle infinie.

        Returns:
        """
        while True:
            self.collection()
            sleep(self.intervalle)


class SenseurTempHum(Senseur):
    """
    La classe qui represente un capteur de temperature DHT-11
    """
    def __init__(self, ids, pin, intervalle, measurement, *args, **kwargs):
        """
        Cree un nouveau SenseurTempHum
        Args:
            ids:        Un identifiant unique pour l'objet
            pin:        Le pin sur lequel le capteur est connecte
            intervalle: L'intervalle a laquelle il faut collecter
                        l'information du capteur en secondes

        Returns:
            None
        """
        self.ids = ids
        self.pin = pin
        self.intervalle = intervalle
        # pylint: disable=no-member
        super().__init__(self.ids, self.pin, intervalle, measurement,
                         *args, **kwargs)

    def collection(self):
        """
        La collection de l'information d'un capteur DHT-11

        La fonction lit la valeur posté par le micro-controlleur
        au pin demandé, puis ajoute les données à la base
        de donné InfluxDB à la table dbname (ici temphum). Elle
        créé la table si elle n'existe pas.

        Returns:
            None
        """
        dbname = "db"
        obj = self.commande(self.pin, 'read')
        try:
            dbs = client.get_list_database()
        except requests.exceptions.ConnectionError:
            log.warning("Waiting for InfluxDB to wake up")
            sleep(0.5)
            return None

        if {'name': dbname} not in dbs:
            client.create_database(dbname)
        client.switch_database(dbname)

        json_body = [{
            'measurement': self.measurement,
            'tags': {
                'node': self.ids,
                'pin': obj['pinNum'],
                'status': obj['status']
            },
            'datetime': str(datetime.now()),
            'fields': {
                'temperature': obj['value']['t'],
                'humidite': obj['value']['h']
            }
        }]
        log.debug(json_body)
        client.write_points(json_body)


class Lampadaire(ObjetIndependant):
    """
    Classe représentant un lampadaire
    """
    def __init__(self, ids, pin, ser=None, *args, **kwargs):
        """
        Créé un nouveau Lampadaire

        Args:
            ids: Un identifiant unique pour l'objet
            pin: Le pin sur lequel la led est connecte
            ser: Non utilise
        """
        self.ids = ids
        self.pin = pin
        self.ser = ser

        self.est_allume = False
        super().__init__(self.ids, *args, **kwargs)

    def allume(self):
        """
        Allume la led

        Envoie un signal au micro-controlleur pour allumer la led
        """
        self.commande(self.pin, 'set', 1)

        self.est_allume = True
        log.debug("Lampadaire est allume")

    def eteind(self):
        """
        Eteind la led

        Envoie un signal au micro-controlleur pour éteindre la led
        """
        self.commande(self.pin, 'set', 0)

        self.est_allume = False
        log.debug("Lampadaire est eteind")

    def controlleur(self):
        """
        L'horaire du lampadaire

        Cette fonction controlle l'allumage de la lampadaire en suivant un
        horaire prédéterminé

        TODO
        """
        log.debug("Controlleur a debute")
        while True:
            num = randint(1, 10)
            if num == 1:
                self.eteind()
            elif num == 10:
                self.allume()
            sleep(1)


class FeuCirculation(Objet):
    """
    Classe representant un feu de circulation
    """
    def __init__(self, ids, *args, **kwargs):
        """
        Créé un nouveau FeuCirculation

        Args:
            ids: Un identifiant unique pour l'objet
        """
        self.etat = 3  # 1: vert, 2: orange, 3: rouge
        self.temps_orange = 3  # temps a passer sur l'orage
        self.ids = ids
        super().__init__(ids, *args, **kwargs)

    def vert(self):
        """
        Change l'etat du feu de circulation a vert
        """
        self.etat = 1

    def rouge(self):
        """
        Change l'état du feu de circulation a rouge

        Avant de devenir rouge, le feu de circulation devient orange
        pour quelque secondes. Afin de guarantir que l'operation
        est non-bloquante, le changement est efectue sur une thread
        independante
        """
        x = threading.Thread(target=self._rougeOrange)
        if self.etat == 1:
            x.start()

    def _rougeOrange(self):
        self.etat = 2
        sleep(self.temps_orange)
        self.etat = 3


class Intersection(Objet):
    """
    Classe représentant une intersection
    """
    def __init__(self, ids, nord, est, sud, ouest, *args, **kwargs):
        """
        Créé une nouvelle Intersection

        Cette fonction initialise les feu de circulation
        en commencant par mettre l'axe nord-sud a rouge
        et l'axe est-ouest a vert

        Args:
            ids: Un identifiant unique pour l'objet
            nord: le FeuCirculation au nord de l'intersection
            est: le FeuCirculation au est de l'intersection
            sud: le FeuCirculation au sud de l'intersection
            ouest: le FeuCirculation au ouest de l'intersection
        """
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
        super().__init__(ids, *args, **kwargs)

    def changeAxe(self):
        """
        Change l'axe de l'intersection

        La fonction s'assure que les FeuCirculation sont tous au rouge
        de changer l'axe
        """
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
