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

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


@app.route('/heroes')
def heroes():
    """
    Returns a list of all heroes in the database.
    """
    heroes = []  # Create an empty list to store the heroes
    for hero in Hero.query.all():  # Iterate over all heroes in the DB 
        hero_dict = {
            "id": hero.id, 
            "name": hero.name,  
            "super_name": hero.super_name
        }
        # Add the hero's dict to the list of heroes
        heroes.append(hero_dict)

    # Create a response that contains the list of heroes
    response = make_response(
        # Convert the list of heroes to JSON
        jsonify(heroes),200
    )
    return response  # Return the response

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    # Query the database for a hero with the given ID
    hero = Hero.query.filter(Hero.id == id).first()
    # If the hero is not found, return a 404 error
    if hero is None:
        response = make_response(
            # Convert the error message to JSON
            jsonify({"error": "Hero not found"}),
            404 )
        return response
    # Convert the hero to a dictionary
    hero_dict = hero.to_dict()
    # Create a response with the hero dictionary
    response = make_response(
        hero_dict, 200) # The hero dictionary
    # Return the response
    return response

@app.route('/powers')
def powers():
    powers = []  # Create an empty list to store the powers
    # Iterate over all powers in the database
    for power in Power.query.all():
        # Create a dictionary to store the power's information,description, id and name
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }
        # Add the dictionary to the list of powers
        powers.append(power_dict)
    response = make_response(
        # Convert the list of powers to JSON
        jsonify(powers),200 )   
    return response

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    # Power does not exist
    if power is None:
        response_body = {"error": "Power not found"}
        # Return the response
        return make_response(response_body, 404)

    if request.method == 'GET':
        # Create a dictionary to store the power's information
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }
        # Return the response
        return make_response(power_dict, 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        if 'description' not in data:
            # Create a response body
            response_body = {"errors": ["description is required"]}
            # Return the response
            return make_response(response_body, 400)
         # Get the description
        description = data['description']
        
        # Validate the description
        if not isinstance(description, str) or len(description) < 20:
            # Create a response body
            response_body = {
                "errors": ["validation errors"]
            }
            # Return the response
            return make_response(response_body, 400)

        # Update the description 
        power.description = description
        db.session.commit()

        # Create a dictionary to store the power's information
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }
        # Return the response
        return make_response(power_dict, 200)
    
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate the  new data
    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        # Return a 400 error with an errors key in the response body
        return make_response({"errors": ["strength, power_id, and hero_id are required"]}, 400)

    # Get the strength, power_id, and hero_id from the request data
    strength = data['strength']
    power_id = data['power_id']
    hero_id = data['hero_id']

    # Check if the Power and Hero exist
    power = Power.query.filter(Power.id == power_id).first()
    hero = Hero.query.filter(Hero.id == hero_id).first()

    # If either the Power or Hero does not exist, return a 404 error
    if not power or not hero:
        return make_response({"errors": ["Power or Hero not found"]}, 404)

    # Validate strength value
    valid_strengths = {"Average", "Strong", "Weak"}
    if strength not in valid_strengths:
        # Return a 400 error with an errors key in the response body
        return make_response({"errors": ["validation errors"]}, 400)

    # Create the new HeroPower instance
    new_hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)

    # Add to the session and commit
    db.session.add(new_hero_power)
    db.session.commit()

    # response data
    response_data = {
        "id": new_hero_power.id,
        "hero_id": hero_id,
        "power_id": power_id,
        "strength": strength,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }
    # Return the response
    return make_response(response_data, 200)
if __name__ == '__main__':
    app.run(port=5555, debug=True)