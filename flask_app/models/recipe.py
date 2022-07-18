from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Recipe:
    schema = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.cooked_at = data['cooked_at']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id"
        results = connectToMySQL(cls.schema).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        recipe = cls(row)
        user_data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        user = User(user_data)
        recipe.user = user
        return recipe

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL(cls.schema).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, cooked_at, under, user_id) VALUES (%(name)s, %(description)s,%(instruction)s, %(cooked_at)s, %(under)s, %(user_id)s) "
        results = connectToMySQL(cls.schema).query_db(query,data)
        return results

    @classmethod
    def edit(cls, data):
        query = "UPDATE recipes SET name = %(name)s,  description = %(description)s,  instruction = %(instruction)s, cooked_at = %(cooked_at)s, under = %(under)s  WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query,data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash(" Name must not be blank!")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must not be blank!")
        if len(recipe['instruction']) < 3:
            is_valid = False
            flash("Instructions must not be blank!")
            
        return is_valid