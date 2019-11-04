from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from api_helpers.mapquestapi import *
from user_helpers.password_hashing import *

# MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.users  # mongoclientstring hidden in config.py

# A runtime-specific dict of user-details, which is populated at login
logged_in_user = None


def add_user(username, email, password, address, isadmin=False):
    """
    This functions creates a user-dictionary from the below-described parameters, and tries to insert it into the db.

    TODO expand this

    :param username: The chosen username
    :type username: str
    :param email: The chosen email
    :type email: str
    :param password: The chosen password
    :type password: str
    :param address: The chosen address
    :type address: str
    :param isadmin: Whether the user is an admin, defaults to False
    :type isadmin: bool
    :return: The inputted user
    :rtype: dict
    """
    hashed_password = hash_password(password)
    timeadded = datetime.now()
    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "address": address,
        "isAdmin": isadmin,
        "location": fetch_coords_from_string(address),
        "Time added": timeadded,
        "Last login": timeadded,
    }

    try:
        db.insert_one(user)
        return user
    except DuplicateKeyError:
        raise ValueError(f'A user with specified username \'{user["username"]}\' or email'
                         f' \'{user["email"]}\' already exists!')


def login(username, password):
    """
    This function allows a user to login, if the username exists, and the password matches the hashed password located
    in MongoDB
    TODO expand + create User-class for the logged-in user!

    :param username: the username which the user tries to log in with
    :type username: str
    :param password: the password which the user tries to log in with
    :type password: str
    :return:
    :rtype:
    """
    result = db.find_one({'username': username})
    if type(result) == dict:
        if verify_password(result["password"], password):
            global logged_in_user
            logged_in_user = result
            return logged_in_user
        else:
            raise ValueError("Password doesn't match username")
    else:
        raise ValueError(f"Username '{username}' doesn\'t exist")


def logout():
    global logged_in_user
    logged_in_user = None


def delete_user(username):
    """
    This function deletes an user from mongoDB

    TODO expand this

    :param username:
    :type username: str
    :raises ValueError:
    :return:
    :rtype: dict
    """
    found_user = db.find_one({"username": username})
    if type(found_user) == dict:
        db.delete_one({"username": username})
        return found_user
    else:
        raise ValueError(f'A user with specified username \'{username}\' does not exist!')
