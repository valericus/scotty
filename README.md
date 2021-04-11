Simple server that stores users with their coordinates and searches for nearest one.
Data is stored in SQLite, file `data.sqlite` in current path. Path to database file
is hardcoded for simplicity.

# How to run

### Install all requirements 
The application uses [Flask](http://flask.pocoo.org/) as web server
and [JSONSchema](https://python-jsonschema.readthedocs.io/) to validate input.
[pytest](https://docs.pytest.org/en/stable/index.html) is also can be useful
to run tests.
```bash
python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip install -r requirements.in/test.txt
```

### Run tests
```bash
$ pytest tests/*
============================= test session starts ==============================
platform linux -- Python 3.8.0, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/valera/code/test_tasks/ntechlab_test_task
collected 8 items                                                              

tests/dao.py ......                                                      [ 37%]
tests/models.py ..

============================== 8 passed in 0.24s ===============================
```

### Start application
```bash
python3 ./ntechlab_test_task.py
```

### Add some users
```bash
$ http POST localhost:5000/add_user "username=James Tiberius Kirk" x_coord:=2 y_coord:=3
HTTP/1.0 200 OK
Content-Length: 59
Content-Type: application/json
Date: Sat, 10 Apr 2021 23:54:44 GMT
Server: Werkzeug/1.0.1 Python/3.8.0

{
    "username": "James Tiberius Kirk",
    "x_coord": 2,
    "y_coord": 3
}

$ http POST localhost:5000/add_user "username=Leonard McCoy" x_coord:=3 y_coord:=2
HTTP/1.0 200 OK
Content-Length: 53
Content-Type: application/json
Date: Sat, 10 Apr 2021 23:55:31 GMT
Server: Werkzeug/1.0.1 Python/3.8.0

{
    "username": "Leonard McCoy",
    "x_coord": 3,
    "y_coord": 2
}

$ http POST localhost:5000/add_user username=Spock x_coord:=13 y_coord:=25
HTTP/1.0 200 OK
Content-Length: 47
Content-Type: application/json
Date: Sat, 10 Apr 2021 23:56:00 GMT
Server: Werkzeug/1.0.1 Python/3.8.0

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
Date: Sat, 10 Apr 2021 23:56:34 GMT
Server: Werkzeug/1.0.1 Python/3.8.0

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
Date: Sat, 10 Apr 2021 23:57:07 GMT
Server: Werkzeug/1.0.1 Python/3.8.0

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
