import requests
import json
from config import *
import re


# TODO: Change quality check (accept P1AXA), and remove 'city' parameter for all geocodings, can we just not use 'city'?

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
    address = f"{business.get('address')},{business.get('zipcode')},DK"
    if "aa" in address or "oe" in address or "aa" in address:
        address = address.replace("aa", "å").replace("ae", "æ").replace("oe", "ø")  # mapquest needs æ ø å
    response = requests.get(
        url='https://www.mapquestapi.com/geocoding/v1/address',
        params={'key': api_mapkey, 'location': address, 'maxResults': 1},
        )
    response_quality = response.json()['results'][0]['locations'][0]['geocodeQualityCode']
    if re.match(r"P1A.A", response_quality) is not None:  # Checks if mapquest is certain
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        business.update({"location": coords})
        business.update({"map url": build_map_url(coords)})
        return business
    else:
        raise ValueError(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")


# TODO: Change quality check (accept P1AXA), and remove 'city' parameter for all geocodings, can we just not use 'city'?

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
    if re.match(r"P1A.A", response_quality) is not None:  # Checks if mapquest is certain
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        return coords
    else:
        print(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")
        raise ValueError(f"Reliable coordinates could not be fetched from given address.")


def build_map_url(coords):
    """
    This functions builds a, basic, Google Maps URL from a set of coordinates. Quite janky.
    TODO reduce jankyness

    :param coords: a 2-dimensional list of longtitude/latitude coordinates
    :type coords: list
    :return: A Google Maps URL
    :rtype: str
    """
    url = f"https://www.google.dk/maps/place/{coords[0]},{coords[1]}"
    return url


def optimize_order(coords_list):
    """

    :param coords_list:
    :type coords_list: list
    :return:
    :rtype: list
    """
    json_input = {"locations": coords_list, "options": {"narrativeType": "none", "doReverseGeocode": "false"}}

    coords_json = json.dumps(json_input)

    response = requests.get(
        url='https://www.mapquestapi.com/directions/v2/optimizedroute',
        params={'key': api_mapkey, 'json': coords_json},
    )

    if response.json()["info"]["statuscode"] == 0:
        optimized_order = response.json()["route"]["locationSequence"]
        optimized_list = []
        for x in optimized_order:
            optimized_list.append(coords_list[x])
        return optimized_list
    else:
        raise ValueError(f'Error from mapquest while generating optimized route: '
                         f'"{response.json()["info"]["messages"][0]}", statuscode: '
                         f'{response.json()["info"]["statuscode"]}')


def create_optimized_url(optimized_coords_list):
    """

    :param optimized_coords_list:
    :type optimized_coords_list: list
    :return:
    :rtype: str
    """
    waypoints_coords = []

    for x in range(1, len(optimized_coords_list) - 1):
        waypoints_coords.append(str(optimized_coords_list[x]))

    waypoints_string = "|"
    waypoints_string = waypoints_string.join(waypoints_coords)

    req = requests.Request('get',
                           url="https://www.google.com/maps/dir/",
                           params={"api": "1",
                                   "origin": optimized_coords_list[0],
                                   "destination": optimized_coords_list[0],
                                   "travelmode": "driving",
                                   "waypoints": waypoints_string}
                           )
    optimized_url = req.prepare().url
    return optimized_url
