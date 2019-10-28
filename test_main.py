from mongofunctions import *
from cvrapi import *
from mapquestapi import *
from datetime import datetime


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

testarg = "Transdesign.dk"

testbusiness = {'vat': 38158686, 'name': 'Transdesign.dk', 'address': 'Langelandsgade 210, st. tv.',
                'zipcode': '8200', 'city': 'Aarhus N', 'protected': False, 'phone': None,
                'email': 'martin@transdesign.dk', 'startdate': '04/11 - 2016', 'employees': None, 'addressco': None,
                'industrycode': 620100, 'industrydesc': 'Computerprogrammering', 'companycode': 10,
                'companydesc': 'Enkeltmandsvirksomhed', 'creditbankrupt': False,
                'owners': [{'name': 'Martin Broholt Trans'}], 'timeadded': datetime(2019, 10, 28, 22, 23, 34, 760576),
                'status': 0, 'note': ''}


def test_delete():
    delete_business(testarg)


def test_business_from_api():
    business_from_api(testarg)


def test_attach_coords():
    attach_coords(testbusiness)


def test_insert_business():
    insert_business(testbusiness)


def test_pull_one():
    pull_single_business(testarg)


def test_pull_all():
    assert {'name': 'Transdesign.dk', 'vat': 38158686} in pull_all_businesses()
