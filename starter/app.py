import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError , requires_auth
from models import db , setup_db , Movie , Actor
from datetime import datetime
def create_app(test_config=None):

  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  db.create_all()


  #fake data 
  Movie(title = 'Godzila' , relaseData = datetime(20,2,11)).insert()
  Actor(name = "Ahmad" , age = 22 , gender = 'M').insert()


  @app.route('/')
  def home():
    movies = Movie.query.all()
    movies = [movie.format() for movie in movies]
    return jsonify({
      'success' : True,
      'movies': movies
    }) , 200 


  @app.route('/movies')
  @requires_auth('get:movies')
  def view_movies(payload):
    movies = Movie.query.all()
    movies = [movie.format() for movie in movies]
    return jsonify({
      'success' : True,
      'movies': movies
    }) , 200 



  @app.route('/actors')
  @requires_auth('get:actors')
  def view_actors(payload):
    actors = Actor.query.all()
    actors = [actor.format() for actor in actors]
    return jsonify({
      'success' : True,
      'movies': actors
    }) , 200 


  @app.route('/movies/create', methods=['POST'])
  @requires_auth('post:movies')
  def post_new_movie(payloads):
      body = request.get_json()
      title = body.get('title', None)
      relaseData = body.get('relaseData', None)
      

      
      if (title == None or relaseData == None ):
        return abort(422)

      movie = Movie( title=title, relaseData=relaseData)
      movie.insert()
      new_movie = Movie.query.get(movie.id)
      new_movie = new_movie.format()

      return jsonify({
        'success': True,
        'created': movie.id,
        'new_movie': new_movie
      })



  @app.route('/actors/create', methods=['POST'])
  @requires_auth('post:actors')
  def post_new_actor(payloads):
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)


      if (name == None or age == None or gender == None):
        return abort(422)

      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()
      new_actor = Actor.query.get(actor.id)
      new_actor = new_actor.format()

      return jsonify({
        'success': True,
        'created': actor.id,
        'new_actor': new_actor
      })


  @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies ')
  def delete_movie(payloads , movie_id):
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if (movie == None):
        return abort(400)

      movie.delete()
      db.session.commit()
      db.session.close()
      return jsonify({
        "success": True,
        "message" : "Delete occured"
      })

  @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payloads , actor_id):
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if (actor == None):
        return abort(400)
      
      actor.delete()
      db.session.commit()
      db.session.close()
      return jsonify({
        "success": True,
        "message" : "Delete occured"
      })

  @app.route('/actors/patch/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(payloads , actor_id):

      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if (actor == None):
        return abort(400)

      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      if (name == None and age == None and gender == None):
        return abort(400)

      actor.name = name
      actor.age = age
      actor.gender = gender
      actor.update()
      return jsonify({
        "success": True,
        "message": "update occured"
      })


  @app.route('/movies/patch/<int:movie_id>' , methods=['PATCH'])
  @requires_auth('patch:movies ')
  def patch_movie(payloads , movie_id):
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if (movie == None):
        return abort(400)

      body = request.get_json()
      title = body.get('title', None)
      relaseData = body.get('relaseData', None)

      if (title == None or relaseData == None):
        return abort(400)
      movie.title = title
      movie.relaseData = relaseData
      movie.update()
      return jsonify({
        "success": True,
        "message": "update occured"
      })




  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code



  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": 'Unathorized'
      }), 401



  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
      }), 422


  @app.errorhandler(400)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "bad request"
      }), 400


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



