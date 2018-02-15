from flask import Flask, jsonify, request, abort
from jsonschema import ValidationError

from model import User, SearchResult

app = Flask(__name__)

storage = dict()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add_user', methods=['POST'])
def add_user():
    if not request.json:
        abort(400, 'Mime type application/json expected')

    try:
        user = User(**request.json)
    except ValidationError as e:
        abort(400, e)

    storage[user.username] = user
    return jsonify(user.to_dict())


@app.route('/get_users')
def get_user():
    if request.args.get('x_coord') and request.args.get('y_coord'):

        try:
            x_coord = float(request.args['x_coord'])
            y_coord = float(request.args['y_coord'])
        except ValueError:
            abort(400, 'Query parameters "x_coord" and "y_coord" are supposed to be numbers')

        result = [SearchResult.for_user(user, x_coord, y_coord) for user in storage.values()]
        result.sort(key=lambda x: x.distance)
    else:
        abort(400, 'Query parameters "x_coord" and "y_coord" are required')

    try:
        count = int(request.args['count'])
    except (KeyError, ValueError):
        count = 100

    return jsonify([i.to_dict() for i in result[:count]])


if __name__ == '__main__':
    app.run()
