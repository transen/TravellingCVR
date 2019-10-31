from mongofunctions import *
from cvrapi import *
from mapquestapi import *
from users import *
from datetime import datetime


testarg = "Transdesign.dk"

testbusiness = {'vat': 38158686, 'name': 'Transdesign.dk', 'address': 'Langelandsgade 210, st. tv.',
                'zipcode': '8200', 'city': 'Aarhus N', 'protected': False, 'phone': None,
                'email': 'martin@transdesign.dk', 'startdate': '04/11 - 2016', 'employees': None, 'addressco': None,
                'industrycode': 620100, 'industrydesc': 'Computerprogrammering', 'companycode': 10,
                'companydesc': 'Enkeltmandsvirksomhed', 'creditbankrupt': False,
                'owners': [{'name': 'Martin Broholt Trans'}], 'timeadded': datetime(2019, 10, 28, 22, 23, 34, 760576),
                'status': 0, 'note': '', 'map url': 'https://www.google.dk/maps/place/56.17339,10.20188'}


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
    assert  type(pull_all_businesses("zipcode")[0]) == dict


def test_delete_user():
    assert type(delete_user("Martin")) == dict


def test_add_user():
    assert type(add_user("Martin", "martin@broholttrans.dk", "test123",
                         "Langelandsgade 210 st tv, 8200 Aarhus N, DK", True)) == dict


def test_login_user():
    assert type(login("Martin", "test123")) == dict


def test_change_status():
    assert type(change_status("Transdesign.dk", 2)) == dict


def test_change_note():
    assert type(change_note("Transdesign.dk", "Test note")) == dict

