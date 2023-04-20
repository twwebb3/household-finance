# models.py
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Sample users (replace this with your own user storage mechanism)
users = [
    User(1, "user1", "password1"),
    User(2, "user2", "password2")
]


def get_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None


def authenticate(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

