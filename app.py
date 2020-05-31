import datetime
import json
from functools import wraps

import jwt
from flask import jsonify, request, Response

from models.MovieModel import Movie
from models.UserModel import User
from settings import *


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'})

    return wrapper


@app.route('/movies')
def get_movies():
    return jsonify({'movies': Movie.get_all_movies()})


@app.route('/movies/<string:imdb_id>')
def get_movie_by_imdb_id(imdb_id):
    return jsonify(Movie.get_movie(imdb_id))


def valid_movie(movie):
    keys = ['name', 'year', 'director', 'imdb_id']
    for key in keys:
        if key not in movie:
            return False
    return True


def valid_put_movie_request_data(movie):
    keys = ['name', 'year', 'director']
    for key in keys:
        if key not in movie:
            return False
    return True


@app.route('/movies', methods=['POST'])
@token_required
def add_movie():
    request_data = request.get_json()
    if valid_movie(request_data):
        Movie.add_movie(request_data['name'], request_data['year'], request_data['director'], request_data['imdb_id'])
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = 'movies/{}'.format(request_data['imdb_id'])
        return response
    else:
        invalid_movie_error_message = {
            'error': 'Invalid movie object passed in request',
            'help_string': 'It should have fields: name, year, director, imdb_id'
        }
        return Response(json.dumps(invalid_movie_error_message), status=400, mimetype='application/json')


@app.route('/movies/<string:imdb_id>', methods=['PUT'])
@token_required
def replace_movie(imdb_id):
    request_data = request.get_json()
    if not valid_put_movie_request_data(request_data):
        invalid_movie_error_msg = {
            'error': 'Invalid movie data passed in request',
            'help_string': 'It should have fields: name, year, director'
        }
        return Response(json.dumps(invalid_movie_error_msg, status=400, mimetype='application/json'))

    Movie.replace_movie(imdb_id, request_data['name'], request_data['year'], request_data['director'])
    return Response('', status=204)


@app.route('/movies/<string:imdb_id>', methods=['PATCH'])
@token_required
def update_movie(imdb_id):
    request_data = request.get_json()
    if 'name' in request_data:
        Movie.update_movie_name(imdb_id, request_data['name'])
    if 'year' in request_data:
        Movie.update_movie_year(imdb_id, request_data['year'])
    if 'director' in request_data:
        Movie.update_movie_director(imdb_id, request_data['director'])

    response = Response('', status=204)
    response.headers['Location'] = 'movies/{}'.format(imdb_id)
    return response


@app.route('/movies/<string:imdb_id>', methods=['DELETE'])
@token_required
def delete_movie(imdb_id):
    if Movie.delete_movie(imdb_id):
        return Response('', status=204)

    invalid_movie_error_message = {
        'error': 'Movie with given imdb_id not found',
        'help_string': 'Provide existing imdb_id'
    }
    return Response(json.dumps(invalid_movie_error_message), status=404, mimetype='application/json')


app.run(port=5000)
