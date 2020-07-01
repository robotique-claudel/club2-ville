import json
import logging
import logging.config
import threading
from time import sleep

from composant import Lampadaire, FeuCirculation, Intersection
from dashboard import app


def main():
    with open('logconfig.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)

    x = threading.Thread(target=app.run_server)
    x.start()

    for i in range(10):
        L = Lampadaire(i)
        L.commence()
        sleep(0.5)

    n = FeuCirculation(1)
    s = FeuCirculation(2)
    e = FeuCirculation(3)
    o = FeuCirculation(4)

    i = Intersection(1, n, e, s, o)


if __name__ == '__main__':
    main()
