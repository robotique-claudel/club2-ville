TODO

Install log driver:
 - `docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions`

Build:
 - `docker-compose up --build [-d]`
 - `docker-compose up`


Test: 
 - `python3 -m unittest discover tests/`
 - `coverage run -m unittest discover tests/`
 - `coverage html`

Queries: 
 - `SELECT "duration" FROM "autogen"."sensor_value" WHERE $timeFilter`