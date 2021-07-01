from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

class Recipe():
    def __init__(self, data):
        self.id = data['recipe_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = None

    @classmethod
    def select_all(cls):
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.users_id;'

        connection = connectToMySQL('recipes')
        results = connection.query_db(query)

        recipes = []

        for result in results:
            recipe = Recipe(result)
            user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            recipe.users_id = Recipe(user_data)
            recipes.append(recipe)
        return recipes

    @classmethod
    def select_by_id(cls, data):
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.users_id WHERE recipes.id = %(id)s;'

        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)
