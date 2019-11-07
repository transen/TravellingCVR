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
        raise ValueError("Business doesn't exist.")  # breaks function and bubbles error to front-end
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        raise ValueError("The businesses' address couldn't be determined")  # breaks function and bubbles error to front-end
    # attempt to insert the business to mongodb
    try:
        business = insert_business(business)
        print(f"'{business['name']}' succesfully inserted!")
        return business
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        raise ValueError("That business already exists in the system!")  # breaks function and bubbles error to front-end


def app_login(username, password):
    result = db.find_one({'username': username})
    if type(result) == dict:
        if verify_password(result["password"], password):  # Move code below to CLI-helper as well + return true/false
            return True
        else:
            raise ValueError("Password doesn't match username")
    else:
        raise ValueError(f"Username '{username}' doesn\'t exist")


def app_change_status(business, new_status):
    try:
        new_status = int(new_status)
        try:
            result = change_status(business, new_status)
            print(f"Status of '{result['name']}' changed to '{result['status']}'!")
            return result
        except ValueError as err:
            print("STATUS-CHANGE ERROR: " + err.args[0])
            raise ValueError(err.args[0])
    except ValueError:
        raise ValueError("Status can only be a number between 1-5")


def app_change_note(business, new_note):
    try:
        result = change_note(business, new_note)
        print(f"Note for '{result['name']}' changed from '{result['note']}' to '{new_note}'")
        return result
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])
        raise ValueError(err.args[0])
