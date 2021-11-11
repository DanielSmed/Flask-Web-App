from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Float)
    unit = db.Column(db.String(10))
    recipe_id = db.Column(db.String, db.ForeignKey('recipe.id'))

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, unique=True, nullable=False)
    recipe_id = db.Column(db.String, db.ForeignKey('recipe.id'))

class Recipe(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(100))
    execution = db.Column(db.String(10000))
    amount = db.Column(db.Integer)

    images = db.relationship('Img')
    ingredients = db.relationship('Ingredient')

    vegetarian = db.Column(db.Boolean)
    vegan = db.Column(db.Boolean)

    milk = db.Column(db.Boolean)
    eggs = db.Column(db.Boolean)
    peanuts = db.Column(db.Boolean)
    soya = db.Column(db.Boolean)
    gluten = db.Column(db.Boolean)
    tree_nuts = db.Column(db.Boolean) # (such as walnuts and cashews)
    fish = db.Column(db.Boolean)
    shellfish = db.Column(db.Boolean)

    privat = db.Column(db.Boolean)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.String, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    privat = db.Column(db.Boolean)
    recipes = db.relationship('Recipe')
    date = db.Column(db.DateTime(timezone=True), default=func.now())
