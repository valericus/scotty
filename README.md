Simple server that stores users with their coordinates and searches for nearest one.
Data is stored in SQLite, file `data.sqlite` in current path. Path to data base file
is hardcoded for simplicity.

# How to run

### Install all requirements 
The application uses [Flask](http://flask.pocoo.org/) as web server
and [JSONSchema](https://python-jsonschema.readthedocs.io/) to validate input.
```bash
pip install -r requirements.txt
```

### Start application
```bash
python3 ./ntechlab_test_task.py
```

### Add some users
```bash
$ http POST localhost:5000/add_user "username=James Tiberius Kirk" x_coord:=2 y_coord:=3
HTTP/1.0 200 OK
Content-Length: 63
Content-Type: application/json
Date: Thu, 15 Feb 2018 15:22:08 GMT
Server: Werkzeug/0.14.1 Python/3.5.2

{
    "username": "James Tiberius Kirk",
    "x_coord": 2,
    "y_coord": 3
}

$ http POST localhost:5000/add_user "username=Leonard McCoy" x_coord:=3 y_coord:=2
HTTP/1.0 200 OK
Content-Length: 63
Content-Type: application/json
Date: Thu, 15 Feb 2018 15:22:08 GMT
Server: Werkzeug/0.14.1 Python/3.5.2

{
    "username": "Leonard McCoy",
    "x_coord": 3
    "y_coord": 2
}

$ http POST localhost:5000/add_user username=Spock x_coord:=13 y_coord:=25
HTTP/1.0 200 OK
Content-Length: 63
Content-Type: application/json
Date: Thu, 15 Feb 2018 15:22:08 GMT
Server: Werkzeug/0.14.1 Python/3.5.2

{
    "username": "Spock",
    "x_coord": 13
    "y_coord": 25
}
```

### Get crew members sorted by distance
Only first 100 members will be returned.
```bash
$ http localhost:5000/get_users x_coord==4 y_coord==5
HTTP/1.0 200 OK
Content-Length: 352
Content-Type: application/json
Date: Thu, 15 Feb 2018 15:33:08 GMT
Server: Werkzeug/0.14.1 Python/3.5.2

[
    {
        "distance": 2.8284271247461903,
        "username": "James Tiberius Kirk",
        "x_coord": 2,
        "y_coord": 3
    },
    {
        "distance": 3.1622776601683795,
        "username": "Leonard McCoy",
        "x_coord": 3,
        "y_coord": 2
    },
    {
        "distance": 21.93171219946131,
        "username": "Spock",
        "x_coord": 13,
        "y_coord": 25
    }
]
```

### Get nearest crew member
```bash
$ http localhost:5000/get_users x_coord==4 y_coord==5 count==1
HTTP/1.0 200 OK
Content-Length: 125
Content-Type: application/json
Date: Thu, 15 Feb 2018 15:47:00 GMT
Server: Werkzeug/0.14.1 Python/3.5.2

[
    {
        "distance": 2.8284271247461903,
        "username": "James Tiberius Kirk",
        "x_coord": 2,
        "y_coord": 3
    }
]
```

Live long and prosper :vulcan_salute:
