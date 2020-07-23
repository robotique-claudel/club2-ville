TODO

Install log driver:
 - `docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions`
ARM
 - `grafana/loki-docker-driver:arm-v7`

Build:
 - `docker-compose up --build [-d]`
 - `docker-compose up`


Test: 
 - `python3 -m unittest discover tests/`
 - `coverage run -m unittest discover tests/`
 - `coverage html`

Queries: 
 - `SELECT "temperature" FROM "temphum"."autogen"."temperature-humidite"`
