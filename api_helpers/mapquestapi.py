import requests
import json
from config import *
import re


def attach_coords(business):
    """
    This function starts off by creating a string being the address of the business, derived from the original
    dictionary served from the CVR-API. It does so by utilizing formatted strings, creating a single string from values
    within the passed business-dictionary.
    This function then queries the MapQuest Geocoding API with an address formatted in a string, and if successful,
    returns a JSON-formatted response including quality, latitude and longtitude. The function then checks the reported
    quality of the response and only if the quality is perfect (=P1A.A), the function will read off the response's
    latitude and longtitude, then save them in a list, which is in the end attached to the business which is returned.
    In the event of MapQuest returning a less-than-perfect quality, the function will raise a ValueError.

    :param business: A dictinary that contains address-, zipcode- and city-key/value-pairs.
    :type business: dict
    :raises: ValueError, if the quality-response is sub-par
    :returns: the business with coordinates attached
    :rtype: dict
    """
    address = f"{business.get('address')},{business.get('zipcode')},DK"
    if "aa" in address or "oe" in address or "aa" in address:
        address = address.replace("aa", "å").replace("ae", "æ").replace("oe", "ø")  # mapquest needs æ ø å
    response = requests.get(
        url='https://www.mapquestapi.com/geocoding/v1/address',
        params={'key': api_mapkey, 'location': address, 'maxResults': 1},
        )
    response_quality = response.json()['results'][0]['locations'][0]['geocodeQualityCode']
    if re.match(r"P1A.A", response_quality) is not None:  # Checks if mapquest is certain, uses regex
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        business.update({"location": coords})
        business.update({"map url": build_map_url(coords)})
        return business
    else:
        raise ValueError(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")


def fetch_coords_from_string(address_string):
    """
    This function queries the MapQuest Geocoding API from an address-string, and if successful,
    returns a JSON-formatted response including quality, latitude and longtitude. The function then checks the reported
    quality of the response, and only if the quality is perfect (=P1A.A), the function will read off the response's
    latitude and longtitude, then save them in a list, which is then returned.
    In the event of MapQuest returning a less-than-perfect quality, the function will raise a ValueError, and an error
    will be logged to the console.

    :param address_string: the adresse in string format, which can be used to fetch the coordinates
    :type address_string: str
    :return: the coordinates of the adress which is input
    :rtype: 
    """
    response = requests.get(
        url='https://www.mapquestapi.com/geocoding/v1/address',
        params={'key': api_mapkey, 'location': address_string, 'maxResults': 1},
    )
    response_quality = response.json()['results'][0]['locations'][0]['geocodeQualityCode']
    if re.match(r"P1A.A", response_quality) is not None:  # Checks if mapquest is certain, uses regex
        lat_lng = response.json()['results'][0]['locations'][0]['latLng']
        coords = list(lat_lng.values())
        return coords
    else:
        print(f"Reliable coordinates could not be fetched from given address, quality: {response_quality}")
        raise ValueError(f"Reliable coordinates could not be fetched from given address: {response_quality}")


def build_map_url(coords):
    """
    This functions builds a, basic, Google Maps URL from a set of coordinates, using formatted strings with a list of
    coordinates as an argument, and returns the URL.

    :param coords: a 2-dimensional list of longtitude/latitude coordinates
    :type coords: list
    :return: A Google Maps URL
    :rtype: str
    """
    url = f"https://www.google.dk/maps/place/{coords[0]},{coords[1]}"
    return url


def optimize_order(coords_list):
    """
    This is the function that generates the optimized order for the locations for solving
    "the travelling salesmen problem", it checks if the statuscode returned by mapquest is = 0 and if it is it checks
    the locationSequence in in the returned JSON file. The locationSequence is the order in which the points are placed
    for the optimized route. If not, a ValueError is raised for handling in the front-end, with additional info.

    :param coords_list: the coordinates required for generating the list
    :type coords_list: list
    :return: a list of coordinates ordered in which route is optimized
    :rtype: list
    """
    json_input = {"locations": coords_list, "options": {"narrativeType": "none", "doReverseGeocode": "false"}}
    coords_json = json.dumps(json_input)
    response = requests.get(
        url='https://www.mapquestapi.com/directions/v2/optimizedroute',
        params={'key': api_mapkey, 'json': coords_json},
    )

    if response.json()["info"]["statuscode"] == 0:  # Quality control
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
    This function constructs a google map url with the optimized route for the buisness selected.
    The passed list of optimized coordinates are converted to strings and put into a new list, except for the user's
    home address, and then joined into a string, separated by the "|"-character, as that's a requirement for the Google
    Maps URL. The function then use the requests-module to generate a request-object, with the appropriate
    HTTP-parameters needed. The URL is then derived as an attribute of the request-object's "prepare()"-method, and
    returned.

    :param optimized_coords_list: list of the optimized coordinates for the route
    :type optimized_coords_list: list
    :return: returns a google maps url with the provided coordinates set to driving
    :rtype: str
    """
    waypoints_coords = []

    for x in range(1, len(optimized_coords_list) - 1):  # The first and the last list-entry are users home-addresses
        waypoints_coords.append(str(optimized_coords_list[x]))

    waypoints_string = "|"  # The character used to separate waypoints in a Google Maps URL
    waypoints_string = waypoints_string.join(waypoints_coords)  # The list of coords is joined into a string, by "|"

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
