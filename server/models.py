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
     # Define the table name in the database
    __tablename__ = 'heroes' 

    # Columns
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String) 
    super_name = db.Column(db.String) 

    # Relationship to HeroPower model
    hero_powers = db.relationship('HeroPower', 
                                  back_populates='heroes',  
                                  cascade="all, delete")  #if a hero is deleted, remove associated hero powers

    # Serialization rules
    # When serializing a hero object, remove the hero_powers column 
    serialize_rules = ('-hero_powers',)

    def __repr__(self):
        return f'<Hero {self.id}>'
# Power Model
class Power(db.Model, SerializerMixin):
    # Define the table name in the database
    __tablename__ = 'powers'  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String)  
    description = db.Column(db.String) 

    # Relationship to HeroPower model
    hero_powers = db.relationship('HeroPower', 
                                  back_populates='power', 
                                  cascade="all, delete")  # If a power is deleted, remove associated hero powers

    # Serialization rules
    # When serializing a power object, remove the hero_powers column
    serialize_rules = ('-hero_powers',)

    # Validation for description
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("validation errors.")
        return description
    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)  
    strength = db.Column(db.String, nullable=False) 
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id')) 
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))  

    # Relationships to Hero and Power models
    heroes = db.relationship('Hero', 
                             back_populates='hero_powers',  
                             cascade="all, delete")  # Cascade deletes for associated hero powers
    power = db.relationship('Power', 
                            back_populates='hero_powers', 
                            cascade="all, delete")  # Cascade deletes for associated hero powers

    # Serialization rules
    # When serializing a hero_power object, remove nested hero_powers columns in  Hero and Power objects
    serialize_rules = ('-heroes.hero_powers', '-power.hero_powers',)
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError 
        return value

    def __repr__(self):
        return f'<HeroPower {self.id}>'
   