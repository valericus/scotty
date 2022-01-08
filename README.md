Simple server that stores users with their coordinates and searches for nearest one. Data is stored
in [PostgreSQL](https://www.postgresql.org/) database. It's picked because it's very common and highly reliable database
engine, also it has wonderful extension [PostGIS](https://postgis.net/) to manage geospatial data.

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

Tests requre running PostgreSQL instance and account permitted to create and drop tables.

```bash
$ pytest --conninfo postgresql://scotty:scotty@localhost:5432/scotty tests/*
============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/valera/code/personal/ntechlab_test_task
collected 5 items                                                                                                                                                           

tests/models.py ..                                                                                                                                                    [ 40%]
tests/user_dao.py ...    

============================== 8 passed in 0.15s ===============================
```

### Start application

First create configuration file, you can use `config.ini-example` as an example.

```bash
cp config.ini-example config.ini
```

Create database and user to use postgres credentials from default config file.

```sql
create table scotty;
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
$ http POST localhost:5000/add_user "username=James Tiberius Kirk" x_coord:=2 y_coord:=3
HTTP/1.0 200 OK
Content-Length: 59
Content-Type: application/json
Date: Sat, 10 Jan 2022 23:54:44 GMT
Server: Werkzeug/2.0.2 Python/3.8.10

{
    "username": "James Tiberius Kirk",
    "x_coord": 2,
    "y_coord": 3
}

$ http POST localhost:5000/add_user "username=Leonard McCoy" x_coord:=3 y_coord:=2
HTTP/1.0 200 OK
Content-Length: 53
Content-Type: application/json
Date: Sat, 10 Jan 2022 23:55:31 GMT
Server: Werkzeug/2.0.2 Python/3.8.10

{
    "username": "Leonard McCoy",
    "x_coord": 3,
    "y_coord": 2
}

$ http POST localhost:5000/add_user username=Spock x_coord:=13 y_coord:=25
HTTP/1.0 200 OK
Content-Length: 47
Content-Type: application/json
Date: Sat, 10 Jan 2022 23:56:00 GMT
Server: Werkzeug/2.0.2 Python/3.8.10

{
    "username": "Spock",
    "x_coord": 13,
    "y_coord": 25
}
```

### Get crew members sorted by distance

Only first 100 members will be returned.

```bash
$ http localhost:5000/get_users x_coord==4 y_coord==5
HTTP/1.0 200 OK
Content-Length: 262
Content-Type: application/json
Date: Sat, 10 Jan 2022 23:56:34 GMT
Server: Werkzeug/2.0.2 Python/3.8.10

[
    {
        "distance": 2.8284271247461903,
        "username": "James Tiberius Kirk",
        "x_coord": 2.0,
        "y_coord": 3.0
    },
    {
        "distance": 3.1622776601683795,
        "username": "Leonard McCoy",
        "x_coord": 3.0,
        "y_coord": 2.0
    },
    {
        "distance": 21.93171219946131,
        "username": "Spock",
        "x_coord": 13.0,
        "y_coord": 25.0
    }
]
```

### Get the nearest crew member

```bash
$ http localhost:5000/get_users x_coord==4 y_coord==5 count==1
HTTP/1.0 200 OK
Content-Length: 95
Content-Type: application/json
Date: Sat, 10 Jan 2022 23:57:07 GMT
Server: Werkzeug/2.0.2 Python/3.8.10

[
    {
        "distance": 2.8284271247461903,
        "username": "James Tiberius Kirk",
        "x_coord": 2.0,
        "y_coord": 3.0
    }
]
```

Live long and prosper :vulcan_salute:
