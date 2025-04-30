"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_get_user():
    users = User.query.all()

    return jsonify(users), 200

@app.route('/user', methods=['GET'])
def handle_user_favs():
    body = request.get_json()
    user_login = body['login']
    
    user = User.query.filter_by(login = user_login).first()
    favorites = user['favorites']

    return jsonify(favorites), 200

@app.route('/people', methods=['GET'])
def handle_get_people():
    people = People.query.all()

    return jsonify(people), 200

@app.route('/people/<int:People_id>', methods=['GET'])
def handle_get_person(People_id):
    people = People.query.filter_by(id = People_id).first()

    return jsonify(people), 200

@app.route('/favorite/people/<int:People_id>', methods=['POST'])
def handle_fav_person(People_id):
    body = request.get_json()
    user_id = body['id']

    newFav = Favorites(user_id = user_id, person_id = People_id, planet_id = None )
    db.session.add(newFav)
    db.session.commit(newFav)

    return jsonify('Favorite has been created'), 200

@app.route('/favorite/people/<int:People_id>', methods=['DELETE'])
def handle_delete_fav_person(People_id):
    body = request.get_json()
    user_id = body['id']

    fav = Favorites.query.filter_by(user_id = user_id, person_id = People_id).first()
    db.session.delete(fav)
    db.session.commit()

    return jsonify('Favorite has been created'), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planets = Planets.query.all()

    return jsonify(planets), 200

@app.route('/planets/<int:Planet_id>', methods=['GET'])
def handle_get_each_planet(Planet_id):
    planet = Planets.query.filter_by(id = Planet_id)

    return jsonify(planet), 200

@app.route('/favorite/planet/<int:Planet_id>', methods=['POST'])
def handle_fav_planet(Planet_id):
    body = request.get_json()
    user_id = body['id']

    newFav = Favorites(user_id = user_id, planet_id = Planet_id, People_id = None )
    db.session.add(newFav)
    db.session.commit(newFav)

    return jsonify('Favorite has been created'), 200

@app.route('/favorite/planet/<int:Planet_id>', methods=['DELETE'])
def handle_delete_fav_planet(Planet_id):
    body = request.get_json()
    user_id = body['id']

    fav = Favorites.query.filter_by(user_id = user_id, planet_id = Planet_id).first()
    db.session.delete(fav)
    db.session.commit()

    return jsonify('Favorite has been created'), 200


















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
