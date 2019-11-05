from api_helpers.mapquestapi import *
from db_helper.mongofunctions import *


def app_add_business(business):
    # TODO check input for valid 8-digit if only digits
    # attempt to grab a business
    try:
        business = business_from_api(business)
        # if business["protected"]:
        #     print("This business is protected against contacting them for ad-purposes.")
        #     sure = input("Are you sure you want to add them to the database? Y/N ")
        #     if sure == "n" or sure == "N":
        #         print(f"'{business['name']}' not added because of protected-status")
        #         return None
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        return ValueError  # breaks function
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        return ValueError  # breaks function
    # attempt to insert the business to mongodb
    try:
        business = insert_business(business)
        print(f"'{business['name']}' succesfully inserted!")
        return business
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return ValueError  # breaks function
