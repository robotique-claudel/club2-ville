import json
import logging
import logging.config

from senseur import initSenseurs


def main():
    with open('config/logconfig.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)

    log = logging.getLogger(__name__)

    log.info("Initialisation des senseurs")
    initSenseurs()


if __name__ == '__main__':
    main()
