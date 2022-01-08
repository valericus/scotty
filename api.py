from flask import Flask, jsonify, request, abort
from jsonschema.exceptions import ValidationError

from dao import UserDAO
from model import User


class Api:
    def __init__(self, dao: UserDAO):
        self.app = Flask(__name__)

        @self.app.route('/add_user', methods=['POST'])
        def add_user():
            if not request.json:
                abort(400, 'Mime type application/json expected')

            try:
                user = User.from_dict(request.json)
            except ValidationError as e:
                abort(400, e)

            dao.save(user)
            return jsonify(user._asdict())

        @self.app.route('/get_users')
        def get_user():
            if request.args.get('lat') and request.args.get('long'):
                try:
                    lat = float(request.args['lat'])
                    long = float(request.args['long'])
                except ValueError:
                    abort(400, 'Query parameters "lat" and "long" are supposed to be numbers')
            else:
                abort(400, 'Query parameters "lat" and "long" are required')

            try:
                count = int(request.args['count'])
            except (KeyError, ValueError):
                count = 100

            result = dao.get_nearest(lat, long, count)

            return jsonify([i._asdict() for i in result])
