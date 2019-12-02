from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from api_helpers.cvrapi import *
from datetime import datetime


db = MongoClient(mongoclientstring).travellingcvr  # mongoclientstring hidden in config.py


def add_errorlog(actor=None, action=None, error=None):
    now = datetime.now()
    error_element = {
        "time": now,
        "user": actor,
        "action": action,
        "error": error
    }
    db.errorlog.insert_one(error_element)


def add_applog(actor=None, action=None, result=None):
    now = datetime.now()
    app_element = {
        "time": now,
        "user": actor,
        "action": action,
        "result": result
    }
    db.applog.insert_one(app_element)
