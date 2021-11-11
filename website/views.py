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

@views.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user == None:
        flash('profile not found', category='error')
        return redirect(url_for('views.home'))
    return render_template('user.html', user=user, cuser=current_user)


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

@views.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        flash('Bad upload!', category='error')
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    
    flash('Img Uploaded!', category='success')
    return 'Img Uploaded!', 200


@views.route('/img/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        flash('Img Not Found!', category='error')
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)