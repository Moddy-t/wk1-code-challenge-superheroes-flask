from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Import necessary modules
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Hero Model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'  # Define the table name in the database

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for hero table
    name = db.Column(db.String)  # Name of the hero
    super_name = db.Column(db.String)  # Superhero name

    # Relationship to HeroPower model
    hero_powers = db.relationship('HeroPower', 
                                  back_populates='heroes',  # Back reference to heroes in HeroPower
                                  cascade="all, delete")  # If a hero is deleted, delete their powers too

    # Serialization rules
    # When serializing a hero object, omit the hero_powers field to avoid circular references
    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        # This method defines how Hero objects are printed (useful for debugging)
        return f'<Hero {self.id}>'
    # This will print something like: <Hero 1> for the hero with ID 1


# Power Model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'  # Define the table name in the database

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for power table
    name = db.Column(db.String)  # Name of the power (e.g., "Invisibility")
    description = db.Column(db.String)  # Description of the power

    # Relationship to HeroPower model
    hero_powers = db.relationship('HeroPower', 
                                  back_populates='power',  # Back reference to power in HeroPower
                                  cascade="all, delete")  # If a power is deleted, remove associated hero powers

    # Serialization rules
    # When serializing a power object, omit the hero_powers field to avoid circular references
    serialize_rules = ('-hero_powers',)

    # Validation for the description field
    @validates('description')
    def validate_description(self, key, description):
        # Ensure the description is at least 20 characters long
        if len(description) < 20:
            raise ValueError("validation errors.")
        return description
    # This will raise a ValueError if the description is too short, ensuring data consistency

    def __repr__(self):
        # This method defines how Power objects are printed (useful for debugging)
        return f'<Power {self.id}>'
    # This will print something like: <Power 1> for the power with ID 1


# HeroPower Model (Associative table for Hero and Power)

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'  # Define the table name in the database

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for hero_powers table
    strength = db.Column(db.String, nullable=False)  # Strength of the power (e.g., "Strong", "Weak", etc.)
    
    # Foreign keys to link to heroes and powers
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))  # Link to hero ID
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))  # Link to power ID

    # Relationships to Hero and Power models
    heroes = db.relationship('Hero', 
                             back_populates='hero_powers',  # Back reference to heroes in Hero
                             cascade="all, delete")  # Cascade deletes for associated hero powers
    power = db.relationship('Power', 
                            back_populates='hero_powers',  # Back reference to powers in Power
                            cascade="all, delete")  # Cascade deletes for associated hero powers

    # Serialization rules
    # When serializing a hero_power object, omit nested hero_powers fields in related Hero and Power objects
    serialize_rules = ('-heroes.hero_powers', '-power.hero_powers',)

    # Validation for the strength field
    @validates('strength')
    def validate_strength(self, key, value):
        # Ensure the strength is one of the allowed values
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError  # Raise an error if the value is invalid
        return value

    def __repr__(self):
        # This method defines how HeroPower objects are printed (useful for debugging)
        return f'<HeroPower {self.id}>'
    # This will print something like: <HeroPower 1> for the hero_power with ID 1

    # add relationships
    # add serialization rules
    # add validatiiom
    def __repr__(self):
        return f'<HeroPower {self.id}>'
