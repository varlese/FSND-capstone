#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from .app import app

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    gender = db.Column(db.String)

    def __repr__(self):
      return f"<Actor id='{self.id}' name='{self.name}'>"

    def to_dict(self):
      return {
        'id': self.id,
        'slug': self.slug,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
      }

# Creating the database for Movies

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    release = db.Column(db.String)

    def to_dict(self):
      return {
        'id': self.id,
        'slug': self.slug,
        'title': self.title,
        'release': self.self,
      }