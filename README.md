Simple service that stores users with their coordinates and searches for nearest one. Data is stored
in [PostgreSQL](https://www.postgresql.org/) database. It's picked because it's very common and highly reliable database
engine, also it has wonderful extension [PostGIS](https://postgis.net/) to manage geospatial data.

Current version is a bit too anthropocentric, as it assumes that coordinates are passed as degrees of latitude and
longitude, and distance is calculated in meters, according to [WGS 84](https://epsg.io/4326). So distances are
calculated correctly only for Earth, but sorting should be more or less correct for any spheroidal planet. Kindly let me
know if you need support of other planets.

There are also some difficulties with performance. Unfortunately there is no plain and simple way to optimise
calculation of distance between two dots on surface, so search of the nearest user has linear difficulty. On the other
hand, ordinary laptop with i7 CPU without any PostgreSQL fine-tuning handles 100k users for about 320 ms, and that looks
acceptable.

# How to run

### Install all requirements

The application uses [Flask](http://flask.pocoo.org/) as web server,
[JSONSchema](https://python-jsonschema.readthedocs.io/) to validate input
and [psycopg3](https://www.psycopg.org/psycopg3/) to connect to PostgreSQL.
[pytest](https://docs.pytest.org/en/stable/index.html) is also can be useful to run tests.

```bash
python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip install -r requirements.in/test.txt
```

### Run tests

Tests requre running PostgreSQL instance with enabled `postgis` extension and account permitted to create and drop
tables.

```bash
$ pytest --conninfo postgresql://scotty:scotty@localhost:5432/scotty tests/*
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0
rootdir: /home/valera/code/personal/scotty
collected 5 items

tests/models.py ..                                                        [ 40%]
tests/user_dao.py ...                                                     [100%]

============================== 5 passed in 0.23s ===============================
```

### Start application

First create configuration file, you can use `config.ini-example` as an example.

```bash
cp config.ini-example config.ini
```

Create database and user to use PostgreSQL credentials from default config file. Create `postgis` extension.

```sql
create database scotty;
\connect scotty
create extension postgis;

create user scotty;
alter database scotty owner to scotty;
\passwd scotty
```

Then start application.

```bash
./scotty.py --config config.ini
```

### Add some users

```bash
$ http POST localhost:5000/add_user "username=James Tiberius Kirk" lat:=2 long:=3
HTTP/1.1 200 OK
Connection: close
Content-Length: 59
Content-Type: application/json
Date: Mon, 27 Mar 2023 00:17:25 GMT
Server: Werkzeug/2.2.3 Python/3.11.2

{
    "username": "James Tiberius Kirk",
    "lat": 2,
    "long": 3
}

$ http POST localhost:5000/add_user "username=Leonard McCoy" lat:=3 long:=2
HTTP/1.1 200 OK
Connection: close
Content-Length: 53
Content-Type: application/json
Date: Mon, 27 Mar 2023 00:17:34 GMT
Server: Werkzeug/2.2.3 Python/3.11.2

{
    "username": "Leonard McCoy",
    "lat": 3,
    "long": 2
}

$ http POST localhost:5000/add_user username=Spock lat:=13 long:=25
HTTP/1.1 200 OK
Connection: close
Content-Length: 40
Content-Type: application/json
Date: Mon, 27 Mar 2023 00:19:05 GMT
Server: Werkzeug/2.2.3 Python/3.11.2

{
    "username": "Spock",
    "lat": 13,
    "long": 25
}
```

### Get crew members sorted by distance

Only first 100 members will be returned.

```bash
$ http GET localhost:5000/get_users lat==4 long==5
HTTP/1.1 200 OK
Connection: close
Content-Length: 234
Content-Type: application/json
Date: Mon, 27 Mar 2023 00:19:38 GMT
Server: Werkzeug/2.2.3 Python/3.11.2

[
    {
        "distance": 313424.65220079,
        "username": "James Tiberius Kirk",
        "lat": 2.0,
        "long": 3.0
    },
    {
        "distance": 349845.80896481,
        "username": "Leonard McCoy",
        "lat": 3.0,
        "long": 2.0
    },
    {
        "distance": 2413163.60819159,
        "username": "Spock",
        "lat": 13.0,
        "long": 25.0
    }
]
```

### Get the nearest crew member

```bash
$ http GET localhost:5000/get_users lat==4 long==5 count==1
HTTP/1.1 200 OK
Connection: close
Content-Length: 85
Content-Type: application/json
Date: Mon, 27 Mar 2023 00:20:04 GMT
Server: Werkzeug/2.2.3 Python/3.11.2

[
    {
        "distance": 313424.65220079,
        "username": "James Tiberius Kirk",
        "lat": 2.0,
        "long": 3.0
    }
]
```

Live long and prosper :vulcan_salute:
