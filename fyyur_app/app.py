#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  jsonify
)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm as Form
from forms import *
from models import *
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

# Use Migrate to track db changes
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Display list of venues
  data = []
  venues = db.session.query(Venue).all()

  # Query db for venues filtered by distinct city and state
  areas = db.session.query(Venue).distinct(Venue.city, Venue.state).all() 

  # Create return object populating fields with areas query
  for area in areas:
    data.append({
      'city': area.city,
      'state': area.state,
      'venues': [{
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': \
          len([show for show in venue.shows \
            if show.start_time > datetime.now()])
      } for venue in venues \
        if venue.city == area.city and venue.state == area.state]
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Implement case-insensitive search query on Venue table with partial string search
  search_term = '%{0}%'.format(request.form.get('search_term'))

  # Query db for search_term
  venues = db.session.query(Venue).filter(Venue.name.ilike(search_term))

  # Create return object populating fields with above search query
  response = {
     'count': venues.count(),
     'data': [{
       'id': venue.id,
       'name': venue.name
      } for venue in venues]
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Shows the venue page with the given venue_id
  # Updates suggested by Udacity reviewer
  
  # Query all for venue_id
  venue = db.session.query(Venue).filter_by(id=venue_id).first_or_404()
  
  past_shows = []
  upcoming_shows = []

  # Populate past_shows and upcoming_shows to data dictionary
  for show in venue.shows:
    temp_show = {
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    if show.start_time <= datetime.now():
      past_shows.append(temp_show)
    else:
      upcoming_shows.append(temp_show)

  # Populate object attributes to data dictionary
  data = vars(venue)

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Create new Venue record in db using form data
  error = False
  form = VenueForm(request.form)

  try:
    # Instaniate new Venue object
    venue = Venue()
    # Populate venue with form data
    form.populate_obj(venue)
    # Add new venue object to database
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except Exception as e:
    error = True
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    # Close database session
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Delete a venue_id record 

  # Query for all venue_id data
  venue = Venue.query.filter_by(id=venue_id).first_or_404()

  try:
    # Remove venue object from db
    db.session.remove(venue)
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully deleted!')
  except Exception as e:
    error = True
    flash('No venue named ' + form.name.data + ' to remove.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    # Close database session
    db.session.close()

  # BONUS CHALLENGE: DELETE BUTTON FUNCTIONALITY

  redirect(url_for('/'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Display list of artists

  # Query db for all artists 
  artists = db.session.query(Artist).all()
  data = []

  # Create return object populating fields with above query
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name,
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Implement case-insensitive search query on Artist table with partial string search
  search_term = '%{0}%'.format(request.form.get('search_term'))
  # Query db for search_term
  artists = db.session.query(Artist).filter(Artist.name.ilike(search_term))

  # Create return object populating fields with above search query
  response = {
    'count': artists.count(),
    'data': [{
      'id': artist.id,
      'name': artist.name
    } for artist in artists]
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # Shows the artist page for artist with ID <artist_id>
  # Updates suggested by Udacity reviewer
  
  # Query all for artist_id
  artist = Artist.query.filter_by(id=artist_id).first_or_404()

  past_shows = []
  upcoming_shows = []
  
  # Populate past_shows and upcoming_shows to data dictionary
  for show in artist.shows:
    temp_show = {
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    }
    if show.start_time <= datetime.now():
      past_shows.append(temp_show)
    else:
      upcoming_shows.append(temp_show)

  # Populate object attributes to data dictionary
  data = vars(artist)

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # Query for all artist_id data
  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  # Populate form with values from artist with ID <artist_id>
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Update existing artist record with ID <artist_id> using the form data
  # Instaniate new Artist object
  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  form = ArtistForm(obj=artist)
  try:
    # Populate artist object with form data
    form.populate_obj(artist)
    # Add new artist object to database
    db.session.add(artist)
    db.session.commit()
    flash('Success! ' + form.name.data + ' has been updated.')
  except Exception as e:
    error = True
    flash('An error occurred. Artist ' + form.name.data + ' could not be edited.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # Query for all venue_id data
  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  # Populate form with values from venue with ID <venue_id>
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # Update existing venue record with ID <venue_id> using the form data

  # Query for all venue_id data
  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  # Populate form with values from venue with ID <venue_id>
  form = VenueForm(obj=venue)

  try:
    # Populate venue object with form data
    form.populate_obj(venue)
    # Add new venue object to database
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except Exception as e:
    error = True
    print(e)
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    # Close database session
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # Create new Venue record in db using form data
  error = False
  form = ArtistForm(request.form)
  
  try:
    # Instaniate new Artist object
    artist = Artist()
    # Populate artist with form data
    form.populate_obj(artist)
    # Add new artist object to database
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully listed!')
  except Exception as e:
    error = True
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    # Close database session
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # Display list of venues

  # Query db for all Show data, joining Venue and Artists tables
  shows = db.session.query(Show).join(Venue, Show.venue_id == Venue.id).join(
        Artist, Artist.id == Show.artist_id).all()
  data = []

  # Create return object populating fields with shows query
  for show in shows:
    # Add show data to return object 
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # Renders form *do not touch*
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # Create new Show record in db using form data
  error = False
  form = ShowForm(request.form)
  
  try:
    # Instaniate new Show object
    show = Show()
    # Populate show with form data
    form.populate_obj(show)
    # Add new show object to database
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    error = True
    flash('An error occurred. Show could not be listed.')
    # Rollback database if update did not complete
    db.session.rollback()
  finally:
    # Close database session
    db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
