from pymongo import MongoClient
from api_helpers.cvrapi import *
from datetime import datetime


db = MongoClient(mongoclientstring).travellingcvr  # mongoclientstring hidden in config.py


def add_errorlog(actor=None, action=None, error=None):
    """
    This functions adds error-logging-capabilites for the webapp. Whenever the functions is called, it logs the current
    time, the actor (who did something), the action (what that person did), and the error (what went wrong), from the
    errors raised down through the stack. All the parameters are optional, and will default to None if nothing is
    passed. It then inserts the error into the error-log-database.


    :param actor: Who did something
    :type actor: str
    :param action: What someone did
    :type action: str
    :param error: What error occurred
    :type error: str
    :return: True
    """
    now = datetime.now()
    error_element = {
        "time": now,
        "user": actor,
        "action": action,
        "error": error
    }
    db.errorlog.insert_one(error_element)
    return True


def add_applog(actor=None, action=None, result=None):
    """
    This functions adds error-logging-capabilites for the webapp. Whenever the functions is called, it logs the current
    time, the actor (who did something), the action (what that person did), and the result (what has changed).
    All the parameters are optional, and will default to None if nothing is passed.  It then inserts the error into
    the app-log-database.

    :param actor: Who did something
    :type actor: str
    :param action: What someone did
    :type action: str
    :param result: What has changed
    :type result: str
    :return: True
    """
    now = datetime.now()
    app_element = {
        "time": now,
        "user": actor,
        "action": action,
        "result": result
    }
    db.applog.insert_one(app_element)
    return True

