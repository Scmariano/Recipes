from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/dashboard')
def recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_id(data)
    recipes = Recipe.get_all()
    return render_template('dashboard.html', recipes = recipes, user=user)


@app.route("/recipe/new")
def new_recipe_form():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    return render_template("create_recipe.html", user=user)


@app.route("/create/recipe", methods=["POST"])
def create_review():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    Recipe.create(request.form)
    return redirect("/dashboard")

@app.route("/recipe/<int:id>")
def show_review(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    review_data = {
        'id': id
    }
    recipe = Recipe.get_one(review_data)
    return render_template("show_recipe.html", recipe=recipe, user=user)

@app.route("/recipe/<int:id>/delete")
def delete(id):
    recipe_data = {
        'id': id
    }
    Recipe.delete(recipe_data)
    return redirect('/dashboard')

@app.route("/recipe/<int:id>/update")
def update(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_id(user_data)
    review_data = {
        'id': id
    }
    recipe = Recipe.get_one(review_data)
    if(recipe.user_id != user.id):
        flash(f"Unauthorized access to edit review with id {id}")
        return redirect("/dashboard")
    return render_template("edit_recipe.html", user=user, recipe=recipe)


@app.route("/recipe/edit/<int:id>", methods = ["POST"])
def edit_recipe(id):
    Recipe.edit(request.form)
    return redirect ("/dashboard")
