#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  genres = db.Column(db.String())
  shows = db.relationship("Show",backref='shows')

# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'Artist'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  shows = db.relationship("Show",backref='show')
  website = db.Column(db.String(120))
  
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  artist_id = db.Column(db.Integer(), db.ForeignKey('Artist.id'),nullable=False)
  venue_id = db.Column(db.Integer(), db.ForeignKey('Venue.id'),nullable=False)
  start_time = db.Column(db.DateTime)


# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
    
db.create_all()
    
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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

  def get_venues(city,state):
      vi = Venue.query.filter(Venue.state==state,Venue.city==city)
      lista = []
      show_count = []
      for i in vi:
        ndict = {}
        ndict['id'] = i.id
        ndict['name'] = i.name
        shows = Show.query.filter_by(venue_id=i.id)
        for i in shows:
          show_count.append(i.id)
        ndict['num_upcoming_shows'] = len(show_count)
        lista.append(ndict)
      return lista


  venue = Venue.query.all()
  location = []
  for i in venue:
    ndict = {}
    ndict["city"] = i.city
    ndict["state"] = i.state
    if ndict not in location:
      location.append(ndict)

  for i in location:
   ndict = {}
   i['venues'] = get_venues(i['city'],i['state'])
   print(i['venues'])
 
  return render_template('pages/venues.html', areas=location);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  venues = Venue.query.all()
  resposta = request.values['search_term']
  data = []

  for i in venues:
    if resposta.casefold() in i.name.casefold():
      ndict= {}
      ndict['id'] = i.id
      ndict['name'] = i.name
      ndict["num_upcoming_shows"] = 0 # to be solved
      data.append(ndict)
   
  
  response2={
    "count": len(data),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response2, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venues = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id = venue_id)
  past_shows = []
  upcoming_shows=[]
  for i in shows:
    ndict = {}
    ndict['artist_id'] = i.artist_id
    dados_artista = Artist.query.get(i.artist_id)
    ndict['artist_name'] = dados_artista.name
    ndict['artist_image_link'] = dados_artista.image_link
    ndict['start_time'] = str(i.start_time)
    if i.start_time < datetime.now():
      past_shows.append(ndict)
    else:
      upcoming_shows.append(ndict)

  data0={
    "id": venue_id,
    "name": venues.name,
    "genres": venues.genres.split(","),
    "address": venues.address,
    "city": venues.city,
    "state": venues.state,
    "phone": venues.phone,
    "website": venues.website,
    "facebook_link": venues.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.", 
    "image_link": venues.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  data = list(filter(lambda d: d['id'] == venue_id, [data0]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  resposta = request.form
  print(resposta)
  venues = Venue(name=resposta['name'],
                  city=resposta['city'],
                  state=resposta['state'],
                  phone=resposta['phone'],
                  genres=resposta['genres'],
                  website=resposta['website'],
                  image_link=resposta['img_link'],
                  facebook_link=resposta['facebook_link'])
  
  try:
    db.session.add(venues)
    db.session.commit()
    flash('Venue ' + resposta['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Venue ' + resposta['name'] + ' was not modified due to an error')
  finally:
    db.session.close()
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return redirect(url_for('index'))

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  print(venue_id)
  venue = Venue.query.get(venue_id)
  show = Show.query.filter_by(venue_id=venue_id)
  for i in show:
    db.session.delete(i)
  db.session.delete(venue)
  db.session.commit()
  flash('Venue ' + resposta['name'] + ' was successfuly deleted')

  return redirect(url_for('index'))
  
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artista = Artist.query.all()
  data2 = []

  for i in artista:
    ndict = {}
    ndict['id'] = i.id
    ndict['name'] = i.name
    data2.append(ndict)

  return render_template('pages/artists.html', artists=data2)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artistas = Artist.query.all()
  resposta = request.values['search_term']
  print(resposta)
  data = []

  for i in artistas:
    if resposta.casefold() in i.name.casefold():
      ndict= {}
      ndict['id'] = i.id
      ndict['name'] = i.name
      ndict["num_upcoming_shows"] = 0
      data.append(ndict)
   
  
  response2={
    "count": len(data),
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response2, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  id = artist_id
  print(id)
  artist = Artist.query.get(artist_id)
  show_data = Show.query.filter_by(artist_id = artist_id )
  past_shows = []
  upcoming_shows = []
  for show in show_data:
    ndict = {}
    ndict["venue_id"] = show.venue_id
    venue = Venue.query.get(show.venue_id)
    ndict["venue_name"] = venue.name
    img_link = Venue.query.get(show.venue_id)
    ndict["venue_image_link"] = img_link.image_link 
    ndict["start_time"] = str(show.start_time)
    if show.start_time <  datetime.now():
      past_shows.append(ndict)
    else:
      upcoming_shows.append(ndict)

  data4={
    "id": id,
    "name": artist.name,
    "genres": artist.genres.split(","),
    "city": artist.city, 
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website, 
    "facebook_link": artist.facebook_link,
    "seeking_venue": True, 
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!", 
    "image_link": artist.image_link, 
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data4)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  artist2={
    "id": artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link":artist.facebook_link,
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": artist.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist2)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artista = Artist.query.get(artist_id)
  resposta = request.values
  print(resposta['img_link'])
  artista.name = resposta['name']
  artista.city = resposta['city']
  artista.state = resposta['state']
  artista.phone = resposta['phone']
  artista.genres = ",".join(resposta.getlist("genres"))
  artista.image_link = resposta['img_link']
  artista.facebook_link = resposta['facebook_link']
  artista.website = resposta['website']
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route("/artists/<int:artist_id>/delete", methods=['POST'])
def delete_artist(artist_id):
  print(artist_id)
  artista = Artist.query.get(artist_id)
  show = Show.query.filter_by(artist_id=artist_id)
  for i in show:
    db.session.delete(i)
  db.session.delete(artista)
  db.session.commit()
  flash('Venue ' + artista.name + ' was successfuly deleted')
  return redirect(url_for("index"))

  
    



    
 

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  venue2={
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": venue.image_link
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  resposta = request.values  
  venue.name = resposta['name']
  venue.city = resposta['city']
  venue.state = resposta['state']
  # venue.address = resposta['address']
  venue.phone = resposta['phone']
  venue.image_link = resposta['img_link']
  venue.facebook_link = resposta['facebook_link']
  venue.website = resposta['website']
  venue.genres = ",".join(resposta.getlist("genres"))
  db.session.commit()
  flash('Venue ' + venue.name + ' was successfully modified!')
      
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  resposta = request.values
  nartist = Artist(name=resposta['name'],
                   city=resposta['city'],
                   state=resposta['state'],
                   phone=resposta['phone'],
                   genres=resposta["genres"],
                   website=resposta["website"],
                   image_link=resposta['img_link'],
                   facebook_link=resposta['facebook_link'])
  print(nartist.name)

  try:
    db.session.add(nartist)
    db.session.commit()
    flash('Artist ' + resposta['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Artist ' + resposta['name'] + ' was not listed due to an error')
  finally:
    db.session.close()
    
  return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()
  data0 = []
  for show in shows:
    ndict={}
    ndict['venue_id'] = show.venue_id
    venue = Venue.query.get(show.venue_id)
    ndict['venue_name'] = venue.name
    ndict['artist_id'] = show.artist_id
    artist = Artist.query.get(show.artist_id)
    ndict['artist_name'] = artist.name
    ndict['artist_image_link'] = artist.image_link
    ndict['start_time'] = str(show.start_time)
    data0.append(ndict)
  return render_template('pages/shows.html', shows=data0)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  resposta = request.form
  nshow = Show(name=resposta['name'],
              artist_id=resposta['artist_id'],
              venue_id=resposta['venue_id'],
              start_time=resposta['start_time'])
  
  try:
    db.session.add(nshow)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
  finally:
    db.session.close()
  
  
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
