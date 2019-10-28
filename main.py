from mongofunctions import *
from cvrapi import *
from mapquestapi import *


def test(testarg="37158686"):
    """
    A function solely to test code written so far, will change over time
    """
    # deletes the business in mongodb if it exists
    try:
        delete_business(testarg)
        print('Deleted business')
    except ValueError as err:
        print(f'Business didn\'t exist: "{err.args[0]}"')
    # attempt to grab a business
    try:
        business = business_from_api(testarg)
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        return None  # breaks function
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        return None  # breaks function
    # attempt to insert the business to mongodb
    try:
        insert_business(business)
        # return business  # to end function
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return None  # breaks function
    # Testing of pull_single_business
    try:
        print(pull_single_business(testarg))
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])
        return None  # breaks function


# test("38158686")


def test2(testarg="38158686"):
    """
    A function solely to test code written so far, will change over time
    """
    # deletes the business in mongodb if it exists
    delete_business(testarg)
    # attempt to grab a business
    business = business_from_api(testarg)
    business = attach_coords(business)
    insert_business(business)
    # return business  # to end function
    print(pull_single_business(testarg))
