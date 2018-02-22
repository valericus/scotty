from flask import Flask, jsonify, request, abort
from jsonschema import ValidationError

from dao import UserDAO
from model import User

app = Flask(__name__)


dao = UserDAO('data.sqlite')


@app.route('/add_user', methods=['POST'])
def add_user():
    if not request.json:
        abort(400, 'Mime type application/json expected')

    try:
        user = User.from_dict(request.json)
    except ValidationError as e:
        abort(400, e)

    dao.save(user)
    return jsonify(user._asdict())


@app.route('/get_users')
def get_user():
    if request.args.get('x_coord') and request.args.get('y_coord'):
        try:
            x_coord = float(request.args['x_coord'])
            y_coord = float(request.args['y_coord'])
        except ValueError:
            abort(400, 'Query parameters "x_coord" and "y_coord" are supposed to be numbers')
    else:
        abort(400, 'Query parameters "x_coord" and "y_coord" are required')

    try:
        count = int(request.args['count'])
    except (KeyError, ValueError):
        count = 100

    result = dao.get_nearest(x_coord, y_coord, count)

    return jsonify([i._asdict() for i in result])


if __name__ == '__main__':
    app.run()
