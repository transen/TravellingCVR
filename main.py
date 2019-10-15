import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import *

# Slår CVR-registret op efter firma-navn og returnerer dict over virksomheden
def cvrapinavn(navn, land='dk'):
    """Looks up the the CVR-register of a company name and returns a dictionary from the API

    :param navn: The name of the company searched for
    :type file_loc: str
    :param land: The country in which one wishes to search for the company in
        (default is 'dk')
    :type print_cols: str
    :returns: A dictionary of the company, served from the API
    :rtype: dict
    """
    response = requests.get(
        url='http://cvrapi.dk/api',
        params={'name': navn, 'country': land},
        headers={'User-Agent': cvr_api_header})
    if response:
        return response.json()
    else:
        print("CVR API Error response:" + str(response))
        raise TypeError("CVR-nummer findes ikke")