import requests
from config import *


def attach_coords(business):
    """
    This function starts off by creating a string being the address of the business, derived from the original
    dictionary served from the API. It does so by utilizing formatted strings, creating a single string from values
    within the passed business-dictionary.
    This function then queries the MapQuest Geocoding API with an address formatted in a string, and if successful,
    returns a JSON-formatted response including quality, latitude and longtitude. The function then checks the reported
    quality of the response and only if the quality is perfect (=P1AAA), the function will read off the response's
    latitude and longtitude, then save them in a list, which is in the end attached to the business which is returned.
    In the event of MapQuest returning a less-than-perfect quality, the function will raise a ValueError.

    TODO Expand error-handling to report which part of the given address-string is unsure about (lists and stuff)
    TODO add comments in code to the docstring

    :param business: A dictinary that contains address-, zipcode- and city-key/value-pairs.
    :type business: dictionary
    :raises ValueError:
    :returns: the business with coordinates attached
    :rtype: dictionary
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
        business.update({"location": coords})
        return business
    else:
        raise ValueError(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")


def fetch_coords_from_string(address_string):
    """

    TODO split the above instead?

    :param address_string:
    :return:
    """
    response = requests.get(
        url='https://www.mapquestapi.com/geocoding/v1/address',
        params={'key': api_mapkey, 'location': address_string, 'maxResults': 1},
    )
    response_quality = response.json()['results'][0]['locations'][0]['geocodeQualityCode']
    if response_quality == "P1AAA":  # Checks if mapquest is certain
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        return coords
    else:
        raise ValueError(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")
