from api_helpers.mapquestapi import *
from db_helper.mongofunctions import *
from user_helpers.users import *
from user_helpers.password_hashing import *


def app_add_business(business):
    # TODO check input for valid 8-digit if only digits
    try:
        business = business_from_api(business)
        # if business["protected"]:  # TODO implement this somehow in front-end?
        #     print("This business is protected against contacting them for ad-purposes.")
        #     sure = input("Are you sure you want to add them to the database? Y/N ")
        #     if sure == "n" or sure == "N":
        #         print(f"'{business['name']}' not added because of protected-status")
        #         return None
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        return ValueError  # breaks function and bubbles error to front-end
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        return ValueError  # breaks function and bubbles error to front-end
    # attempt to insert the business to mongodb
    try:
        business = insert_business(business)
        print(f"'{business['name']}' succesfully inserted!")
        return business
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return ValueError  # breaks function and bubbles error to front-end


def app_login(username, password):
    result = db.find_one({'username': username})
    if type(result) == dict:
        if verify_password(result["password"], password):  # Move code below to CLI-helper as well + return true/false
            return True
        else:
            raise ValueError("Password doesn't match username")
    else:
        raise ValueError(f"Username '{username}' doesn\'t exist")
