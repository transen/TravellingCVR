from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from api_helpers.mapquestapi import *
from user_helpers.password_hashing import *

#: MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.users  # mongoclientstring hidden in config.py

#: A runtime-specific dict of user-details, which is populated at login, only eligible for CLI-version
logged_in_user = None


def add_user(username, email, password, address, isadmin=False):
    """
    This functions creates a user-dictionary from the below-described parameters, and tries to insert it into the db.
    It uses the datetime-module to capture the current time, and saves that as 'Time added' and 'Last login'.
    If an error occurs during insertion of the user, the function will faise a ValueError.

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
        "username": username.capitalize(),
        "email": email.capitalize(),
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
    in MongoDB, only eligible for CLI-version.

    :param username: the username which the user tries to log in with
    :type username: str
    :param password: the password which the user tries to log in with
    :type password: str
    :return: the logged in user
    :rtype: dict
    """
    result = db.find_one({"username": {'$regex': username, '$options': 'i'}})
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
    This function deletes an user from mongoDB. It checks whether the requested user for deletion exists, and if it does
    the user will be deleted, otherwise a ValueError is raised.

    :param username: the username of the active user
    :type username: str
    :raises ValueError: if no user with the specified username is found
    :return: returns the dictionary with the deleted username
    :rtype: dict
    """
    found_user = db.find_one({"username": {'$regex': username, '$options': 'i'}})
    if type(found_user) == dict:
        db.delete_one({"username": username})
        return found_user
    else:
        raise ValueError(f'A user with specified username \'{username}\' does not exist!')


def update_user_last_login(username):
    """
    This function updates the "last login" attribute in the db. It's executed everytime a user successfully logs in
    from the front end app.

    :param username: The username of the active user
    :type username: str
    :raises ValueError: if user can't be found
    :return: the updated user-dict from DB
    :rtype: dict
    """
    user = db.find_one({"username": {'$regex': username, '$options': 'i'}})
    if user:
        last_login = datetime.now()
        result = db.find_one_and_update(
            {"username": username},
            {"$set":
             {"Last login": last_login}
             })
        return result
    else:
        raise ValueError("User doesn't exist.")


def pull_user(username):
    """
    Pulls a user from the database, returns the user if it exists, otherwise it raises an ValueError.
    
    :param username: The username of the active user
    :type username: str
    :raises ValueError: if user can't be found
    :return: dictionary of the specified user
    :rtype: dict
    """
    user = db.find_one({"username": {'$regex': username, '$options': 'i'}})
    if user:
        return user
    else:
        raise ValueError("User doesn't exist.")
