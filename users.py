from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from mapquestapi import *
from password_hashing import *

# MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.users  # mongoclientstring hidden in config.py

# A runtime-specific array of user-details, which is populated at login
logged_in_user = []


def add_user(username, email, password, address, isadmin):
    """
    This functions creates a user-dictionary from the below-described parameters, and tries to insert it into the db.

    TODO expand this

    :param username: The wanted username
    :type username: str
    :param email:
    :type email: str
    :param password:
    :type password: str
    :param address:
    :type address: str
    :param isadmin:
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

    TODO expand + create User-class for the logged-in user!

    :param username:
    :type username: str
    :param password:
    :type password: str
    :return:
    :rtype:
    """
    result = db.find_one({'username': username})
    if type(result) == dict:
        if verify_password(result["password"], password):
            print("*login*")
            global logged_in_user
            logged_in_user = [username, result["email"], result["address"]]
            return logged_in_user
        else:
            print("Wrong password")
    else:
        print("Username not found!")


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
