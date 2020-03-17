#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

database_name = "agency"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
moment = Moment()

# Set-up database-related Flask modules. 
def setup_db(app, database_path=database_path):
	app.config.from_pyfile('config.py', silent=False)
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	moment.app = app
	db.init_app(app)
	db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Placeholder for future database that potentially connects actors to movies (based on Genre database from prior project)

# class Genre(db.Model):
#   __tablename__ = 'Genre'

#   id = db.Column(db.Integer, primary_key = True)
#   name = db.Column(db.String(), nullable = False)
#   slug = db.Column(db.String(), unique = True, nullable = False)

# # Creating relationship to connect Genre categories to Venue table
# venue_genre_relationship = db.Table('venue_genre_relationship',
#     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
#     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete = 'cascade')),
#     db.Column('id', db.Integer, primary_key = True)
# )

# # Creating relationship to connect Genre categories to Artist table
# artist_genre_relationship = db.Table('artist_genre_relationship',
#     db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id')),
#     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete = 'cascade')),
#     db.Column('id', db.Integer, primary_key = True)
# )

# Creating the debatase for Actors

class Actor(db.Model):
	__tablename__ = 'actors'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	age = db.Column(db.String)
	gender = db.Column(db.String)

	def __repr__(self):
		return f"<Actor id='{self.id}' name='{self.name}'>"

	def __init__(self, name, age, gender):
		self.name = name
		self.age = age
		self.gender = gender

	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
		'id': self.id,
		'name': self.name,
		'age': self.age,
		'gender': self.gender
		}

# Creating the database for Movies

class Movie(db.Model):
	__tablename__ = 'movies'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	release = db.Column(db.String)

	def __repr__(self):
		return f"<Movie id='{self.id}' title='{self.title}'>"

	def insert(self):
		db.session.add(self)
		db.session.commit()
	
	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
		'id': self.id,
		'title': self.title,
		'release': self.release,
		}