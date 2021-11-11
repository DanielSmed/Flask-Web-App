from flask import Blueprint, render_template, request, Response, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Recipe, Img, User, Ingredient
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", cuser=current_user, recipes=Recipe.query.order_by(Recipe.date).all())

# -- user handeling --

@views.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user == None:
        flash('profile not found', category='error')
        return redirect(url_for('views.home'))
    return render_template('user.html', user=user, cuser=current_user)

# -- recipe handeling --

@views.route('/edit/<ID>', methods=['GET', 'POST'])
@login_required
def edit_recipe(ID):
    if request.method == 'POST':
        
        recipe = Recipe.query.get(ID)

        if current_user.id != recipe.user_id:
            flash('not your recipe.', category='error')
            return redirect(url_for('views.edit_recipe', ID=recipeId))
        else:

            recipe.title = request.form.get('title')
            recipe.amount = request.form.get('amount')
            recipe.execution = request.form.get('execution')

            recipe.vegetarian = True if request.form.get('vegetarian') == 'vegetarian' else False
            recipe.vegan = True if request.form.get('vegan') == 'vegan' else False

            recipe.milk = True if request.form.get('milk') == 'milk' else False
            recipe.eggs = True if request.form.get('eggs') == 'eggs' else False
            recipe.peanuts = True if request.form.get('peanuts') == 'peanuts' else False
            recipe.soya = True if request.form.get('soya') == 'soya' else False
            recipe.gluten = True if request.form.get('gluten') == 'gluten' else False
            recipe.tree_nuts = True if request.form.get('tree_nuts') == 'tree_nuts' else False
            recipe.fish = True if request.form.get('fish') == 'fish' else False
            recipe.shellfish = True if request.form.get('shellfish') == 'shellfish' else False

            recipe.privat = True if request.form.get('privat') == 'privat' else False

            db.session.commit()
            flash('Recipe updated!', category='success')
            return redirect(url_for('views.recipe', ID=ID))
    else:
        if ID == "0":
            new_recipe= Recipe(privat=False, user_id=current_user.id)
            db.session.add(new_recipe)
            db.session.commit()
            recipe = current_user.recipes[len(current_user.recipes)-1]
            flash('New recipe created!', category='success')
            return redirect(url_for('views.edit_recipe', ID=recipe.id))
        else:
            recipe = Recipe.query.filter_by(id=ID).first()
            if recipe == None:
                flash('recipe not found', category='error')
                return redirect(url_for('views.user', username=current_user.user_name))
            elif recipe.user_id != current_user.id:
                flash('not your recipe', category='error')
                return redirect(url_for('views.home'))
        return render_template('edit_recipe.html', recipe=recipe, cuser=current_user)

@views.route('/recipe/<ID>', methods=['GET', 'POST'])
def recipe(ID):
    recipe = Recipe.query.filter_by(id=ID).first()
    if recipe == None:
        flash('recipe not found', category='error')
        return redirect(url_for('views.home'))
    return render_template('recipe.html', recipe=recipe, cuser=current_user)

@views.route('/delete-recipe', methods=['POST'])
@login_required
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    flash(recipeId, category='error')
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
    else:
        flash("recipe not found", category='error')

    return jsonify({})

# -- image handeling --

@views.route('/upload/<recipeId>', methods=['POST'])
@login_required
def upload(recipeId):
    pic = request.files['pic']
    if not pic:
        flash('No pic uploaded!', category='error')
        return redirect(url_for('views.edit_recipe', ID=recipeId))

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        flash('Bad upload!', category='error')
        return redirect(url_for('views.edit_recipe', ID=recipeId))

    elif mimetype != "image/jpeg" and mimetype != "image/png":
        flash('not a .png or .jpg', category='error')
        return redirect(url_for('views.edit_recipe', ID=recipeId))

    img = Img(img=pic.read(), name=filename, mimetype=mimetype, recipe_id=recipeId)
    db.session.add(img)
    db.session.commit()
    
    flash('Img Uploaded!', category='success')
    return redirect(url_for('views.edit_recipe', ID=recipeId))

@views.route('/img/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        flash('Img Not Found!', category='error')
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

# -- ingredient handeling --

@views.route('/add/<recipeId>', methods=['POST'])
@login_required
def add(recipeId):
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        unit = request.form.get('unit')

        recipe = Recipe.query.get(recipeId)

        if current_user.id != recipe.user_id:
            flash('not your recipe.', category='error')
            return redirect(url_for('views.edit_recipe', ID=recipeId))
        else:
            new_ingredient = Ingredient(name=name, amount=amount, unit=unit, recipe_id=recipeId)
            db.session.add(new_ingredient)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.edit_recipe', ID=recipeId))
        
    return redirect(url_for('views.edit_recipe', ID=recipeId))