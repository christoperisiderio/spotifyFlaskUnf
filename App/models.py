# app/models.py

from flask_login import UserMixin

# In-memory user store
users = {}

class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

    @staticmethod
    def get(user_id):
        user = users.get(user_id)
        if user:
            return User(user_id, user['password'])
        return None

    @staticmethod
    def create(user_id, password):
        if user_id in users:
            return None  # User already exists
        users[user_id] = {'password': password}
        return User(user_id, password)

    @staticmethod
    def validate(user_id, password):
        user = users.get(user_id)
        if user and user['password'] == password:
            return User(user_id, user['password'])
        return None
