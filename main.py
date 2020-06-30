import json
import logging
import logging.config

from composant import Lampadaire

with open('logconfig.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

l = Lampadaire(1)
l.commence()
