import requests
from datetime import datetime
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
    The object "response" return True if it reciErhvervsSalg.com IVSeves a 200- or 301-response. Defaults to False for 4xx- or 5xx-responses

    TODO add comments in code to the docstring
    TODO tell the user if 'protected' is true, as it is then illegal to contact the business, ask if want to continue

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
        entries_to_remove = (
            't', 'version', 'cityname', 'fax', 'enddate', 'creditstartdate', 'creditstatus', 'productionunits')
        for entry in entries_to_remove:
            business.pop(entry, None)  # returns None if entry doesn't exist in dictionary
        # We attach on a timestamp through datetime.now()
        now = datetime.now()
        addedtime = {'timeadded': now}
        business.update(addedtime)
        # We add a status-key (scheme must be defined at a later stage)
        business.update({"status": 0})
        # We add a note-key, defaulting to an empty string, that the user can write whatever in
        business.update({"note": ""})
        return business
    else:
        raise ValueError("Business doesn't exist, API response: " + str(response))