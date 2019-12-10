from user_helpers.password_hashing import *


class User():
    """
    User class required for flask-login to function, allows a logged-in-user-session to be constructed. Assigns username
    as user ID.
    """
    def __init__(self, username):
        self.username = username
        self.email = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return verify_password(password, password_hash)
