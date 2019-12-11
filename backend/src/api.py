"""
**Introduction**
----------------
The coffee shop app is a new digitally enabled cafe for udacity students
to order drinks, socialize, and study hard. The full stack drink menu
application with the following endpoints implemented:

- GET /drinks
- GET /drinks-detail
- POST /drinks
- PATCH /drinks/<id>
- DELETE /drinks/<id>

With the following API permissions:
- `get:drinks-detail` (Barista and Manager)
- `post:drinks` (Manager)
- `patch:drinks` (Manager)
- `delete:drinks` (Manager)

"""

import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import NotFound

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# CORS Headers

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ----------------------------------------------------------------------------#
# uncomment the following line to initialize the datbase
# ----------------------------------------------------------------------------#
db_drop_and_create_all()

# ----------------------------------------------------------------------------#
# Helper Functions
#    dump: print out the contents of an object
#    paginate: pages data for output
#    leftJoin does a database left join on sets
# ----------------------------------------------------------------------------#


def dumpObj(obj):
    for attr in dir(obj):
        print('obj.%s = %r' % (attr, getattr(obj, attr)))


def dumpData(obj):
    for attr in obj:
        print('data.%s = %r' % (attr, obj[attr]))


# ----------------------------------------------------------------------------#
# ----------------------------------------------------------------------------#
# ROUTES
# ----------------------------------------------------------------------------#
# ----------------------------------------------------------------------------#

# ----------------------------------------------------------------------------#
#  Get list of Drinks - Short form, public
# ----------------------------------------------------------------------------#

@app.route('/drinks', methods=['GET'])
def list_of_drinks_short_form():
    """
        **Get Drinks**

        Get a list of the drinks in short form

        **Get Drinks**

        - Sample Call create question::

            curl -X POST http://localhost:5000/drinks
                 -H 'content-type: application/json'


        - Expected Success Response::

            HTTP Status Code: 200

            {
             "success": true,
             "drinks": [ list of drink.short() ]
            }


        - Expected Fail Response::

            HTTP Status Code: 401
            {
                "description": "401: Authorization header is expected.",
                "error": 401,
                "message": "Unauthorized",
                "success": false
            }

    """

    selection = Drink.query.order_by(Drink.id).all()
    drinks_list = [d.short() for d in selection]

    if selection is None:
        abort(404)

    return jsonify({'success': True, 'drinks': drinks_list})


# ----------------------------------------------------------------------------#
#  Retrieve list of drinks in long form.
# ----------------------------------------------------------------------------#

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def list_of_drinks_long_form(payload):
    """
        **Retrieve Drink Details in Long form**

        Get a list of the drinks in long form

        **Get Drinks**

        - Sample Call create question::

            curl -X POST http://localhost:5000/drinks
                 -H 'content-type: application/json'


        - Expected Success Response::

            HTTP Status Code: 200

            {
            "drinks": [
                {
                "id": 1,
                "recipe": [
                    {
                    "color": "white",
                    "name": "Vodka",
                    "parts": 1.5
                    },
                    {
                    "color": "red",
                    "name": "Cranberry Juice",
                    "parts": 1
                    }
                ],
                "title": "Cosmo"
                }
            ],
            "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 401
            {
                "description": "401: Authorization header is expected.",
                "error": 401,
                "message": "Unauthorized",
                "success": false
            }
   """

    selection = Drink.query.order_by(Drink.id).all()

    if selection is None:
        abort(404)

    drinks = [d.long() for d in selection]

    return jsonify({'success': True, 'drinks': drinks})


# ----------------------------------------------------------------------------#
#  Create drink
# ----------------------------------------------------------------------------#

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_new_drink(payload):
    """
        **Create Drink**

        This API will create a new Drink.

        **Create a new Drink**

        - Sample Call create drink::

            curl -X POST http://localhost:5000/drinks \
                 -H 'content-type: application/json' \
                 -d '{"title": "Water3", \
                      "recipe": [{"name": "Water", \
                                 "color": "blue", \
                                 "parts": 1 \
                                }] \
                    }'

        - Expected Success Response::

            HTTP Status Code: 200

            {
            "drinks": {
                "id": 2,
                "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
                ],
                "title": "Water"
            },
            "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 401
            {
                "description": "401: Authorization header is expected.",
                "error": 401,
                "message": "Unauthorized",
                "success": false
            }
    """

    request_json = request.get_json()

    try:

        # The request JSON is passed to be initialized by Question
        # class's __init__

        title = request_json.get('title', None)
        recipe = request_json.get('recipe', None)

        drink = Drink(title=title, recipe=recipe)
        drink.insert()

        return jsonify({'success': True, 'drinks': drink.long()})
    except Exception:
        abort(422)


# ----------------------------------------------------------------------------#
#  Update Drink
# ----------------------------------------------------------------------------#

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    """
        **Updates a drink**

        This API will update a drink by drink Id.

        - Sample Call::

            curl -X PATCH http://localhost:5000/drink/1 \
                 -H 'content-type: application/json' \
                 -d '{"title": "water"}'

        - Expected Success Response::

            HTTP Status Code: 200

            {
            "drinks": [
                {
                "id": 1,
                "recipe": [
                    {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                    }
                ],
                "title": "water"
                }
            ],
            "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 401
             {
                "description": "401: Authorization header is expected.",
                "error": 401,
                "message": "Unauthorized",
                "success": false
            }
    """

    # Get the drink record

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    # Abort if no drink found

    if drink is None:
        abort(404)

    request_json = request.get_json()
    title = request_json.get('title', None)
    recipe = request_json.get('recipe', None)

    # Set the values

    if title is not None:
        drink.title = title
    if recipe is not None:
        drink.recipe = recipe

    # do the update

    try:
        drink.update()

    except Exception as e:
        abort(422)

    return jsonify({'success': True, 'drinks': [drink.long()]})


# ----------------------------------------------------------------------------#
#  Delete question from the database
# ----------------------------------------------------------------------------#

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    """
        **Delete a drink from the database**

        This API will delete a drink from the database.

        - Sample Call::

            curl -X DELETE http://localhost:5000/drink/2
                 -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200
            {
                "deleted": 2,
                "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 401
            {
                "description": "401: Authorization header is expected.",
                "error": 401,
                "message": "Unauthorized",
                "success": false
            }
    """

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({'success': True, 'deleted': drink_id})
    except NotFound:
        abort(404)
    except Exception as e:

        abort(422)


# ------------------------------------------------------------------------#
#  error handlers
# ------------------------------------------------------------------------#

@app.errorhandler(400)
def bad_request(error):
    return (jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request',
        'description': str(error),
        }), 400)


@app.errorhandler(401)
def unauthorized_user(error):
    return (jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized',
        'description': str(error),
        }), 401)


@app.errorhandler(404)
def not_found(error):
    return (jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found',
        'description': str(error),
        }), 404)


@app.errorhandler(405)
def not_found(error):
    return (jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed',
        'description': str(error),
        }), 405)


@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable',
        'description': str(error),
        }), 422)


@app.errorhandler(500)
def unprocessable(error):
    return (jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error',
        'description': str(error),
        }), 500)
