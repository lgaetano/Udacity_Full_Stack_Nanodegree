from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

# Define models
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='venue', lazy="joined")

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    
    shows = db.relationship('Show', backref='artist', lazy="joined")

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)