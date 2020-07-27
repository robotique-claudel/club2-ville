import composant as c


def initSenseurs():
    c.SenseurTempHum("temp1", 2, 2, "temperature-humidite").commence()
