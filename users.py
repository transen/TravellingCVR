import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import *
import hashlib, binascii, os

logged_in_user = []

# https://www.vitoshacademy.com/hashing-passwords-in-python/ -kilde


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


# MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.users  # mongoclientstring hidden in config.py


def add_user(username, email, password, address, isadmin):
    hashed_password = hash_password(password)
    timeadded = datetime.now()
    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "address": address,
        "isAdmin": isadmin,
        "Time added": timeadded,
        "Last login": timeadded,
    }

    try:
        result = db.insert_one(user)
        print(f"Inserted user with the id: {result.inserted_id}")
        return result
    except DuplicateKeyError:
        raise ValueError(f'A user with specified username \'{user["username"]}\' or email \'{user["email"]}\' already exists!')


def login(username, password):
    result = db.find_one({'username': username})
    if type(result) == dict:
        if verify_password(result["password"], password):
            print("*login*")
            logged_in_user = [username, result["email"], result["address"]]
        else:
            print("Wrong password")
    else:
        print("Username not found!")


while True:
    print('What action would you like to perform?')
    print('1: Add user')
    print('2: Log in')
    wanted_action = int(input('Choose between 1-2: '))
    if wanted_action == 1:
        chosen_username = input("Input username: ")
        chosen_email = input("Input email: ")
        chosen_password = input("Input password: ")
        chosen_address = input("Input address: ")
        isAdmin = False
        try:
            add_user(chosen_username, chosen_email, chosen_password, chosen_address, isAdmin)
        except ValueError as err:
            print("ERROR", err.args[0])
        want_again = input("Want to do another operation? Y/N")
        if want_again == 'y' or want_again == 'Y':
            continue
        else:
            break
    elif wanted_action == 2:
        try_username = input("Input username: ")
        try_password = input("Input password: ")
        login(try_username, try_password)
        want_again = input("Want to do another operation? Y/N")
        if want_again == 'y' or want_again == 'Y':
            continue
        else:
            break
    else:
        print("Not understood, try again.")
