import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import *


def cvr_api_name(name, country='dk'):
    """
    Looks up the CVR-register of a company name and returns a dictionary from the API, operated by a third party.
    The API responds to a HTTP GET- or POST-query, with the inclusion of a search-parameter, a name in this case. It
    also requires a country-parameter, which we've set to default to 'dk' for Denmark.
    The API respodns to other parameters as well, but we've omitted them,
    as they're optional and not relevant for this project. It also requires an User-Agent in the header.
    See documentation here: https://cvrapi.dk/documentation (only in Danish, however).
    The function relies on the module 'requests', which handles HTTP for python, and we utilize the .json()-method, to
    decode the JSON response to a dictionary. If the HTTP-request returns a response including a vat-key, the function
    will return the business-info as a dictionary. If not, the function will print the response-error to the console.
    The object "response" return True if it recieves a 200- or 301-response. Defaults to False for 4xx- or 5xx-responses

    #TODO Delete this one? Doesn't seem to work, and might be redundant anyway... Move documentation to VAT-version

    :param name: The name of the company searched for, must be an exact match
    :type name: str
    :param country: The country in which one wishes to search for the company in, defaults to 'dk')
    :type country: str, optional
    :raises TypeError: The business doesn't exist
    :return: A dictionary of the company, served from the API
    :rtype: dictionary
    """
    response = requests.get(
        url='https://cvrapi.dk/api',
        params={'name': name, 'country': country},
        headers={'User-Agent': cvr_api_header})
    if 'vat' in response:
        return response.json()
    else:
        print("CVR API Error response:" + str(response))
        raise TypeError("Business doesn't exist")


def cvr_api_vat(vat, country='dk'):
    """
    Same as function 'cvrapiname()' but with a VAT-number as the search-parameter.

    :param vat: The VAT-number of the company searched for
    :type vat: int
    :param country: The country in which one wishes to search for the company in, defaults to 'dk')
    :type country: str, optional
    :raises TypeError: The business doesn't exist
    :returns: A dictionary of the company, served from the API
    :rtype: dictionary
    """
    response = requests.get(
        url='https://cvrapi.dk/api',
        params={'search': vat, 'country': country},
        headers={'User-Agent': cvr_api_header})
    if 'vat' in response.json():
        return response.json()
    else:
        print("CVR API Error response:" + str(response))
        raise TypeError("Business doesn't exist")


def create_address_string(business):
    """
    This function creates and returns a string being the address of the business, derived from the original
    dictionary served from the API. It does so by utilizing formatted strings, creating a single string from values
    within the passed business-dictionary.

    :param business: A dictinary that contains address-, zipcode- and city-key/value-pairs.
    :type business: dictionary
    :returns: An address-string, which is compatible with the MapQuest API
    :rtype: str
    """
    adress_string = f"{business.get('address')},{business.get('zipcode')},{business.get('city')},DK"
    return adress_string


def final(vat):
    business = cvr_api_vat(vat)
    print(create_address_string(business))


final(38158686)
