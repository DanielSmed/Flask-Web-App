from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Ingredient(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.float)
    unit = db.Column(db.String(10))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Image(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image = (db.longblob)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    execution = db.Column(db.String(10000))
    images = db.relationship('Image')
    ingredients = db.relationship('Ingredient')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    recipes = db.relationship('Recipe')
