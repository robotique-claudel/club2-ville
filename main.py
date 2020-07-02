import json
import logging
import logging.config
import serial
import threading
from time import sleep

from composant import Lampadaire, FeuCirculation, Intersection
from dashboard import app


def main():
    with open('logconfig.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
    
    log = logging.getLogger(__name__)


    x = threading.Thread(target=app.run_server, kwargs={'host': '0.0.0.0'})
    x.start()

    sleep(1)

    sers = {}
    with open("pinconfig.json", "r") as f:
        config = json.load(f)
    
    for i in config.keys():
        try:
            sers[i] = serial.Serial(i, 9600)
            sers[i].baudrate = 9600
        except serial.serialutil.SerialException:
            log.error("Erreur dans l'ouverture du port: %s", i)
            sers[i] = None

        for j in config[i]['pins']:
            if j['type'] == 'lampadaire':
                if sers[i] != None:
                    l = Lampadaire(j['id'], j['pinNum'], ser=sers[i])
                    l.commence()
                else: 
                    log.warning("Passe l'objet %s au port %d avec id %s car le port serial n'existe pas", j['type'], j['pinNum'], j['id'])


        
    n = FeuCirculation(1)
    s = FeuCirculation(2)
    e = FeuCirculation(3)
    o = FeuCirculation(4)

    i = Intersection(1, n, e, s, o)

    

if __name__ == '__main__':
    main()
