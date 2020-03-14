#----------------------------------------------------------------------------#
# Config.
#----------------------------------------------------------------------------#

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask_sqlalchemy import SQLAlchemy
from .models import Actor, Movie, db
from .auth.auth import AuthError, requires_auth, get_token_auth_header

## ---------------------------------------------------------
## ROUTES
## ---------------------------------------------------------

# TODO: Create formatting for actors and movies.
# GET endpoint for list of actors in database.
@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()

    if not actors:
        abort(404)

    return jsonify({
        'success': True,
        'actors': [actor for actor in actors]
    }), 200

# GET endpoint for list of movies in database.
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    if not movies:
        abort(404)

    return jsonify({
        'success': True,
        'movies': [movie for movie in movies]
    }), 200

# POST endpoint to add an actor to the database.
# TODO: Permissions (Casting Director)
@app.route('/add-actor', methods=['POST'])
#@requires_auth('post:actors')
def add_actor():
    data = request.get_json()

    if 'name' not in data:
        abort(422)
    if 'age' not in data:
        abort(422)
    if 'gender' is not data:
        abort(422)

    actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
    actor.insert()

    return jsonify({
        'success': True,
        'actor': actor,
    }), 200

# POST endpoint to add a movie to the database.
# TODO: Permissions (Executive Producer)
@app.route('/add-movie', methods=['POST'])
#@requires_auth('post:movies')
def add_movie():
    data = request.get_json()

    if 'title' not in data:
        abort(422)
    if 'release' not in data:
        abort(422)

    movie = Movie(title=data['title'], release=data['release'])
    movie.insert()

    return jsonify({
        'success': True,
        'movie': movie,
    }), 200

# PATCH endpoint to update an actor in the database.
# TODO: Permissions (Casting Director)
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
#@requires_auth('patch:actor')
def update_actor(actor_id):
    if not actor_id:
        abort(404)

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)

    data = request.get_json()

    if 'name' in data and data['name']:
        actor.name = data['name']

    if 'age' in data and data['age']:
        actor.age = data['age']

    if 'gender' in data and data['gender']:
    	actor.gender = data['gender']

    actor.update()

    return jsonify({
        'success': True,
        'actor': actor,
    }), 200

# PATCH endpoint to update a movie in the database.
# TODO: Permissions (Casting Director)
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
#@requires_auth('patch:actor')
def update_movie(movie_id):
    if not movie_id:
        abort(404)

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)

    data = request.get_json()

    if 'title' in data and data['title']:
        movie.name = data['title']

    if 'release' in data and data['release']:
        movie.release = data['release']

    movie.update()

    return jsonify({
        'success': True,
        'movie': movie,
    }), 200

# DELETE endpoint to delete actors in the database.
# TODO: Permissions (Casting Director)
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
#@requires_auth('delete:actor')
def delete_actor(actor_id):
    if not actor_id:
        abort(404)

    actor_to_delete = Actor.query.get(actor_id)
    if not actor_id:
        abort(404)

    actor_to_delete.delete()
    db.session.commit()

    return jsonify({
        'success': True,
        'delete': actor_id
    }), 200

# DELETE endpoint to delete movies in the database.
# TODO: Permissions (Executive Producer)
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
#@requires_auth('delete:movie')
def delete_movie(movie_id):
    if not movie_id:
        abort(404)

    movie_to_delete = Movie.query.get(movie_id)
    if not movie_id:
        abort(404)

    movie_to_delete.delete()
    db.session.commit()

    return jsonify({
        'success': True,
        'delete': movie_id
    }), 200

## ---------------------------------------------------------
## Error Handling
## ---------------------------------------------------------
@app.errorhandler(401)
def not_authorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Authentication error."
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "Forbidden."
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Item not found."
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Request could not be processed."
    }), 422

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

