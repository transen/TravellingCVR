from mongofunctions import *
from cvrapi import *
from mapquestapi import *


# def test(testarg="37158686"):
#     """
#     A function solely to test code written so far, will change over time
#     """
#     # deletes the business in mongodb if it exists
#     try:
#         delete_business(testarg)
#         print('Deleted business')
#     except ValueError as err:
#         print(f'Business didn\'t exist: "{err.args[0]}"')
#     # attempt to grab a business
#     try:
#         business = business_from_api(testarg)
#     except ValueError as err:
#         print("API ERROR: " + err.args[0])
#         return None  # breaks function
#     # attempt to fetch coordinates
#     try:
#         business = attach_coords(business)
#     except ValueError as err:
#         print("COORDS ERROR: " + err.args[0])
#         return None  # breaks function
#     # attempt to insert the business to mongodb
#     try:
#         insert_business(business)
#         # return business  # to end function
#     except ValueError as err:
#         print("INSERT ERROR: " + err.args[0])
#         return None  # breaks function
#     # Testing of pull_single_business
#     try:
#         print(pull_single_business(testarg))
#     except ValueError as err:
#         print("PULL ERROR: " + err.args[0])
#         return None  # breaks function


# test("38158686")


# def test_full_stack(testarg="Transdesign"):
#     delete_business(testarg)
#     business = business_from_api(testarg)
#     business = attach_coords(business)
#     insert_business(business)
#     pull_single_business(testarg)


def test_delete(testarg="Transdesign.dk"):
    delete_business(testarg)


def test_business_from_api(testarg="Transdesign.dk"):
    business_from_api(testarg)


def test_attach_coords(testarg="Transdesign.dk"):
    attach_coords(business_from_api(testarg))


def test_insert_business(testarg="Transdesign.dk"):
    insert_business(attach_coords(business_from_api(testarg)))


def test_pull_one(testarg="Transdesign.dk"):
    pull_single_business(testarg)


def test_pull_all():
    assert {'name': 'Transdesign.dk', 'vat': 38158686} in pull_all_businesses()
