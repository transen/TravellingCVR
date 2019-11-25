from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from api_helpers.cvrapi import *
import datetime


db = MongoClient(mongoclientstring).travellingcvr  # mongoclientstring hidden in config.py


def add_errorlog(actor, action, result):
    now = datetime.now()
    error_element = {
        "now": now,
        "actor": actor,
        "action": action,
        "result": result
    }
    try:
        db.errorlog.insert_one(error_element)
    except DuplicateKeyError as err:
        raise ValueError(f"Something went wrong inserting error to log: {err}")


def add_applog(actor, action, result):
    now = datetime.now()
    app_element = {
        "now": now,
        "actor": actor,
        "action": action,
        "result": result
    }
    try:
        db.applog.insert_one(app_element)
    except DuplicateKeyError as err:
        raise ValueError(f"Something went wrong inserting action to applog: {err}")
