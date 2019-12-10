from db_helper.mongofunctions import *
from api_helpers.cvrapi import *
from user_helpers.users import *
from datetime import datetime


# This module is purely here for the case of trying out Test Driven Development, set up with PyTest.

#: Test-argument used in PyTest
testarg = "Transdesign.dk"

#: Test-argument used in PyTest
testbusiness = {'vat': 38158686, 'name': 'Transdesign.dk', 'address': 'Langelandsgade 210, st. tv.',
                'zipcode': '8200', 'city': 'Aarhus N', 'protected': False, 'phone': None,
                'email': 'martin@transdesign.dk', 'startdate': '04/11 - 2016', 'employees': None, 'addressco': None,
                'industrycode': 620100, 'industrydesc': 'Computerprogrammering', 'companycode': 10,
                'companydesc': 'Enkeltmandsvirksomhed', 'creditbankrupt': False,
                'owners': [{'name': 'Martin Broholt Trans'}], 'timeadded': datetime(2019, 10, 28, 22, 23, 34, 760576),
                'status': 0, 'note': '', 'map url': 'https://www.google.dk/maps/place/56.17339,10.20188'}

#: Test-argument used in PyTest
test_list_vats = [34709912, 27746802, 35898743, 39387786]

#: Test-argument used in PyTest
test_coords_list = ['56.17339,10.20188', '57.04825,9.94738', '55.85552,9.65243',
                    '56.17284,10.19938', '56.17339,10.20188']


def test_delete_business():
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
    assert type(pull_all_businesses("zipcode")[0]) == dict


def test_delete_user():
    assert type(delete_user("Martin")) == dict


def test_add_user():
    assert type(add_user("Martin", "martin@broholttrans.dk", "test123",
                         "Langelandsgade 210 st tv, 8200, DK", True)) == dict


def test_login_user():
    assert type(login("Martin", "test123")) == dict


def test_change_status():
    assert type(change_status("Transdesign.dk", 2)) == dict


def test_change_note():
    assert type(change_note("Transdesign.dk", "Test note")) == dict


def test_pull_user():
    assert pull_user("mArtin")["email"] == "Martin@broholttrans.dk"


def test_db_search():
    assert len(search_businesses("trans")) == 1


def test_db_vat_to_coords():
    assert len(vat_to_coords(test_list_vats)) == 4


def test_optimize_order():
    assert optimize_order(test_coords_list) == test_coords_list


def test_create_optimized_url():
    assert create_optimized_url(test_coords_list) == "https://www.google.com/maps/dir/?api=1&" \
                                                     "origin=56.17339%2C10.20188&" \
                                                     "destination=56.17339%2C10.20188&travelmode=driving&" \
                                                     "waypoints=57.04825%2C9.94738%7C55.85552%2C9.65243%7C" \
                                                     "56.17284%2C10.19938"

