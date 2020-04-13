# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from .app import create_app
from .models import setup_db, Actor, Movie

# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_should_return_all_actors(self):
        # Insert dummy actor into database.
        actor = Actor(name="Leonardo Di Caprio", age="45", gender="male")
        actor.insert()

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_get_actors_dont_accept_post_request(self):
        res = self.client().post('/actors')
        self.assertEqual(res.status_code, 405)

    def test_should_return_all_movies(self):
        # Insert dummy actor into database.
        movie = Movie(title="Devil Wears Prada", release="June 30, 2006")
        movie.insert()

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_get_movies_dont_accept_post_request(self):
        res = self.client().post('/movies')
        self.assertEqual(res.status_code, 405)

    def test_should_create_new_actor(self):
        new_actor_data = {
            'name': "New actor name worked.",
            'age': "New actor age worked.",
            'gender': "New actor gender worked."
        } 

        res = self.client().post('/add-actor', data=json.dumps(new_actor_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor_data['name'])
        self.assertEqual(data['actor']['age'], new_actor_data['age'])
        self.assertEqual(data['actor']['gender'], new_actor_data['gender'])

        actor_added = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor_added)

    def test_should_not_allow_new_actor_missing_age(self):
        new_actor_data = {
            'name': "Testing a new actor with missing data.",
            'gender': "male"
        } 

        res = self.client().post('/add-actor', data=json.dumps(new_actor_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_should_create_new_movie(self):
        new_movie_data = {
            'title': "New movie title worked.",
            'release': "New movie release date worked.",
        }

        res = self.client().post('/add-movie', data=json.dumps(new_movie_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], new_movie_data['title'])
        self.assertEqual(data['movie']['release'], new_movie_data['release'])

        movie_added = Movie.query.get(data['movie']['id'])
        self.assertTrue(movie_added)

    def test_should_not_allow_new_movie_missing_date(self):
        new_movie_data = {
            'title': "Testing a new movie with missing data."
        } 

        res = self.client().post('/add-movie', data=json.dumps(new_movie_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_should_update_existing_actor_data(self):
        actor = Actor(name="Anne Hathaway", age="50", gender="female")
        actor.insert()

        actor_data_patch = {
            'age': '37'
        } 

        res = self.client().patch(
            f'/actors/%s' % (actor.id),
            data=json.dumps(actor_data_patch),
            headers={'Content-Type': 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor_data_patch['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)

    def test_should_not_update_existing_actor_if_not_found(self):
        actor_data_patch = {
            'age': '1'
        } 

        res = self.client().patch('/actors/9999', data=json.dumps(actor_data_patch), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_delete_existing_actor(self):
        actor = Actor(name="Anne Hathaway", age="37", gender="female")
        actor.insert()

        res = self.client().delete(f'/actors/%s' % actor.id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    def test_should_not_delete_existing_actor_if_not_found(self):
        res = self.client().delete('/actors/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_update_existing_movie_data(self):
        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()

        movie_data_patch = {
            'release': 'March 20, 2020'
        } 

        res = self.client().patch(
            f'/movies/%s' % (movie.id),
            data=json.dumps(movie_data_patch),
            headers={'Content-Type': 'application/json'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], movie_data_patch['release'])

        movie_updated = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie_updated.id, movie.id)

    def test_should_not_update_existing_movie_if_not_found(self):
        movie_data_patch = {
            'title': 'Foo'
        } 

        res = self.client().patch('/movies/9999', data=json.dumps(movie_data_patch), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_delete_existing_movie(self):
        movie = Movie(title="Invisible Man", release="March 20, 2020")
        movie.insert()

        res = self.client().delete(f'/movies/%s' % movie.id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)

    def test_should_not_delete_existing_movie_if_not_found(self):
        res = self.client().delete('/movies/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
