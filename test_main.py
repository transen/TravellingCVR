from mongofunctions import *
from cvrapi import *
from mapquestapi import *
from datetime import datetime


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
