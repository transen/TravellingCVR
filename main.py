import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import *


def business_from_api(vat_or_name, country='dk'):
    """
    Looks up the CVR-register of a company name OR VAT and returns a dictionary from the API, operated by a third party.
    The API responds to a HTTP GET- or POST-query, with the inclusion of a search-parameter, a name or VAT in this case.
    It also requires a country-parameter, which we've set to default to 'dk' for Denmark.
    The API responds to other parameters as well, but we've omitted them,
    as they're optional and not relevant for this project. It also requires an User-Agent in the header.
    See documentation here: https://cvrapi.dk/documentation (only in Danish, however).
    The function relies on the module 'requests', which handles HTTP for python, and we utilize the .json()-method, to
    decode the JSON response to a dictionary. If the HTTP-request returns a valid response, the function
    will return the business-info as a dictionary. If not, the function will print the response-error to the console
    and raise a ValueError.
    The object "response" return True if it recieves a 200- or 301-response. Defaults to False for 4xx- or 5xx-responses

    TODO add comments in code to the docstring

    :param vat_or_name: The name or VAT (8 digits) of the company searched for, must be an exact match
    :type vat_or_name: int or str
    :param country: The country in which one wishes to search for the company in, defaults to 'dk')
    :type country: str, optional
    :raises ValueError: The business doesn't exist
    :return: A dictionary of the company, served from the API
    :rtype: dictionary
    """
    response = requests.get(
        url='https://cvrapi.dk/api',
        params={'search': vat_or_name, 'country': country},
        headers={'User-Agent': cvr_api_header})
    if response:
        business = response.json()
        # We clear out the information we don't need
        entries_to_remove = ('t', 'version', 'cityname', 'fax', 'enddate', 'creditstartdate', 'creditstatus', 'productionunits')
        for entry in entries_to_remove:
            business.pop(entry, None)
        # We attach on a timestamp through datetime.now()
        now = datetime.now()
        addedtime = {'timeadded': now}
        business.update(addedtime)
        # We add a status-key (scheme must be defined at a later stage)
        business.update({"status": 0})
        # We add a note-key, defaulting to an empty string, that the user can write whatever in
        business.update({"note": ""})
        print(business) # delete me at some point
        return business
    else:
        print("CVR API Error response: " + str(response))
        raise ValueError("Business doesn't exist")


def fetch_coords(business):
    """
    This function starts off by creating a string being the address of the business, derived from the original
    dictionary served from the API. It does so by utilizing formatted strings, creating a single string from values
    within the passed business-dictionary.
    This function then queries the MapQuest Geocoding API with an address formatted in a string, and if successful,
    returns a JSON-formatted response including quality, latitude and longtitude. The function then checks the reported
    quality of the response and only if the quality is perfect (=P1AAA), the function will read off the response's
    latitude and longtitude, and save them in a list, which is in the end returned.
    In the event of MapQuest returning a less-than-perfect quality, the function will raise a ValueError.

    TODO Expand error-handling to report which part of the given address-string is unsure about (lists and stuff)
    TODO add comments in code to the docstring

    :param business: A dictinary that contains address-, zipcode- and city-key/value-pairs.
    :type business: dictionary
    :raises ValueError:
    :returns: a set of coordinates in a list
    :rtype: list
    """
    address = f"{business.get('address')},{business.get('zipcode')},{business.get('city')},DK"
    if "aa" in address or "oe" in address or "aa" in address:
        address = address.replace("aa", "å").replace("ae", "æ").replace("oe", "ø")  # mapquest needs æ ø å
    response = requests.get(
        url='https://www.mapquestapi.com/geocoding/v1/address',
        params={'key': api_mapkey, 'location': address, 'maxResults': 1},
        )
    response_quality = response.json()['results'][0]['locations'][0]['geocodeQualityCode']
    if response_quality == "P1AAA":  # Checks if mapquest is certain
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        return coords
    else:
        print(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")
        raise ValueError(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")


def test(testarg):
    """
    A function solely to test code written so far, will change over time
    """
    business = business_from_api(testarg)
    print(fetch_coords(business))


test("34709912")
