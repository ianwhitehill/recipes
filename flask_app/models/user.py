from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)

        users = []

        for item in results:
            user = User(item)
            users.append(user)

        return users

    @classmethod
    def insert(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)
        return results

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) == 0 or len(data['first_name']) > 45:
            is_valid = False
            flash("First name must not be empty and must be 45 characters or less.")

        if len(data['last_name']) == 0 or len(data['last_name']) > 45:
            is_valid = False
            flash("Last name must not be empty and must be 45 characters or less.")

        if len(data['email']) == 0 or len(data['email']) > 255:
            is_valid = False
            flash("Email must not be empty and must be 255 characters or less.")

        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be greater then 8 characters")

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Password did not match confirm password")

        if len(User.get_by_email(data)) > 0:
            is_valid = False
            flash("User with this Email already exists")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Invalid email address!")

        return is_valid