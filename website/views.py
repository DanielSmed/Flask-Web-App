from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Recipe
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        recipe = request.form.get('recipe')

        if len(recipe) < 1:
            flash('Recipe is too short!', category='error')
        else:
            new_recipe = Recipe(data=recipe, user_id=current_user.id)
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-recipe', methods=['POST'])
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipe']
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()

    return jsonify({})
