#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Import necessary modules
from flask import Flask, request, jsonify, make_response
from models import db, Hero, Power, HeroPower  # Assuming you have these models defined elsewhere

# Initialize the Flask application
app = Flask(__name__)

# Basic Route


# Root route that returns a simple message
@app.route('/')
def index():
    return '<h1>Code challenge</h1>'



# GET /heroes - Retrieve all heroes
@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    # Retrieve all hero objects from the database
    heroes = Hero.query.all()
    # Convert each hero object to a dictionary using to_dict method 
    # and return the list as a response with a 200 OK status code
    return make_response([hero.to_dict() for hero in heroes], 200)
# GET /heroes by id- Retrieve hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_heroes_by_id(id):
    # Query the database to find the hero by the provided ID
    heroes = Hero.query.filter_by(id=id).first()
    # If a hero with the provided ID is found
    if heroes:
        # Convert hero to a dictionary
        heroes = heroes.to_dict()
        # Retrieve all associated hero powers from HeroPower table for this hero
        hero_powers = HeroPower.query.filter_by(hero_id=id).all()
        # Add the hero_powers data to the hero dictionary as a list 
        heroes['hero_powers'] = [hero_power.to_dict() for hero_power in hero_powers]
        
        # Return the hero data and a 200 OK status
        return heroes, 200
    else:
        return {'error': 'Hero not found'}, 404

# GET /powers - Retrieve all powers
@app.route('/powers', methods=['GET'])
def get_all_powers():
    # Retrieve all power objects from the database
    powers = Power.query.all()
    # Convert each power object to a dictionary and return the list as a response
    return make_response([power.to_dict() for power in powers], 200)

# GET  Retrieve power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_powers_by_id(id):
    # Query the database to find the power by the provided ID
    powers = Power.query.filter_by(id=id).first()
    # If the power is not found;
    if powers is None:
        return make_response({'error': 'Power not found'}, 404)
    else:
        # If found, convert it to a dictionary and return it
        return make_response(powers.to_dict(), 200)


# PATCH  Update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_powers(id):
    # Query the database to find the power by the provided ID
    power = Power.query.get(id)
    # If the power is not found;
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    # Get the new description from the request.json.get method
    description = request.json.get('description')
    # description should be at least 20 characters long
    if description and len(description) < 20:
        return jsonify({'errors': ["validation errors"]}), 400
    # Update the power's description
    power.description = description
    # Commit the changes to the db
    db.session.commit()
    # Return the updated power details with a 200 OK status
    return jsonify(power.to_dict()), 200
# POST /hero_powers - Create a new hero-power relationship


@app.route('/hero_powers', methods=['POST'])
def post_hero_powers():
    if request.method == 'POST':
        # Create a new HeroPower relationship from the JSON request body, get strength,hero_id && power_id
        hero_power = HeroPower(
            strength=request.json['strength'],  
            hero_id=request.json['hero_id'],    
            power_id=request.json['power_id']   
        )
        # Add the new hero_power to the session and commit it to db
        db.session.add(hero_power)
        db.session.commit()
        # Return the newly created hero_power data as a response
        return make_response(hero_power.to_dict(), 200)
    else:
        return make_response({'error': '[validation errors]'}, 405)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
