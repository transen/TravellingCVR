from pymongo import MongoClient, ReturnDocument
from pymongo.errors import DuplicateKeyError
from api_helpers.cvrapi import *

# MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.businesses  # mongoclientstring hidden in config.py


def insert_business(business):
    """
    This function inserts a business into the mongodb, via the module "Pymongo" which bridges the gap between python and
    and the hosted MongoDB-database. MongoDB is inherently noSQL, compared to a traditional relational SQL-database,
    which we are accustomed to, and used to work with. This has been an intentionally added challenge, in order to
    obtain more practical knowledge of noSQL-moddeled behaviour in regards to non-structured data.
    

    :param business: it's a dictonary of a buisness with all the data included
    :type business: dict
    :raises ValueError: if a buisness with the the identifier (vat) already exists it raises a valueError
    :return: returns the dictonary again so it can be presented to the user, much like a callback
    :rtype: dictonary
    """
    try:
        db.insert_one(business)
        return business
    except DuplicateKeyError:
        raise ValueError(f'A business with the VAT \'{business["vat"]}\' already exists!')


def pull_single_business(searchable):
    """
    Pulls a single business from MongoDB from VAT-parameter or name of business
    
    :param searchable: The search-term inputted by the end-user
    :type searchable: str
    :raises ValueError: if no business in DB found with that name or VAT
    :return: The queried business
    :rtype: dictionary
    """
    if type(searchable) == str and searchable.isdigit():
        searchable = int(searchable)
    result = db.find_one({"$or": [{"vat": searchable}, {"name": searchable}]})
    if type(result) == dict:
        # converts timestamp to a human-readable timestring
        result['timeadded'] = result['timeadded'].strftime("%d-%m-%y %H:%M")
        return result
    else:
        raise ValueError(f'No business found in DB with VAT or name: "{searchable}"')


def pull_all_businesses(sorted_by="name"):
    """
    This functions pulls all businesses in MongoDB and returns a list of businesses as output.
    the list includes all data regarding the businesses, it's done by simply running a for loop through
    all entries in the database and then appending it to a list one by one. This insures that everytime
    a new buisness is created it will always get pulled with this function.


    :param sorted_by: just there to sort each buisness by the name
    :type sorted_by: str
    :raises ValueError:
    :return: A list of all businesses located in the database.
    :rtype: list
    """

    result = list(db.find({}).sort(sorted_by, 1))
    if type(result) == list:
        output = []
        for business in result:
            output.append(business)
        return output
    else:
        raise ValueError("Something went wrong")


def delete_business(searchable):
    """
    This function aims to delete a business from the MongoDB, if it exists. It starts off checking whether the queried
    business exists in the DB. If 'result' returns a dictionary, the business exists, and utilizes the built-in pymongo
    "delete_one"-method to delete the business-document from the DB. The function then returns the deleted business,
    for further handling and presentation to the end-user.

    :param searchable: The search-term inputted by the end-user
    :type searchable: str
    :raises ValueError: If no buisness with the provided name or VAT is found
    :return: The business which has just been deleted
    :rtype: dictionary
    """
    if type(searchable) == str and searchable.isdigit():
        searchable = int(searchable)
    result = db.find_one({"$or": [{"vat": searchable}, {"name": searchable}]})
    if type(result) == dict:
        db.delete_one({"$or": [{"vat": searchable}, {"name": searchable}]})
        return result
    else:
        raise ValueError(f'No business found in DB with VAT or name: {searchable}')


def search_businesses(searchable):
    """
    This functions runs a $search query on mongodb, through a $text-index, and returns a list of dictionaries,
    which are the individual businesses queried by the searchable. The searchable is checked whether it is supposed
    to be a VAT (if it's a string, only digits and lenght is 8), and is then handled as and converted to int, querying
    the mongodb only for VAT-fields. If the result is empty (len = 0) a ValueError is raised, which is handled later on
    by either front-end (Flask or CLI). Otherwise the result is pakced into a list and returned.

    :param searchable: The search-term inputted by the end-user
    :type searchable: str
    :raises ValueError: When result is empty
    :return: A list of businesses in dict-form
    :rtype: list
    """
    if type(searchable) == str and searchable.isdigit() and len(searchable) == 8:
        # if searchable matches above, it is a VAT
        searchable = int(searchable)
        results = list(db.find({"vat": searchable}))
    else:
        results = list(db.find({"$text": {"$search": searchable}}))
    if len(results) != 0:
        for result in results:
            # converts timestamp to a human-readable timestring
            result['timeadded'] = result['timeadded'].strftime("%d-%m-%y %H:%M")
        return results
    else:
        raise ValueError(f'No business found in DB when searching for: "{searchable}"')


def change_status(searchable, wanted_status):
    """
    This function changes the status of a business in the mongodb.

    :param searchable: The search-term inputted by the end-user
    :type searchable: str or int
    :param wanted_status: number between 1-5
    :type wanted_status: int
    :return: The updated business
    :rtype: dict
    """
    if type(searchable) == str and searchable.isdigit():
        searchable = int(searchable)
    business = db.find_one({"$or": [{"vat": searchable}, {"name": searchable}]})
    if business:
        business_id = business['_id']
        result = db.find_one_and_update(
            {"_id": business_id},
            {"$set":
                {"status": wanted_status}
             }, return_document=ReturnDocument.AFTER)
        return result
    else:
        raise ValueError("Business doesn't exist.")


def change_note(searchable, wanted_note):
    """
    This function changes the note of a business in the mongodb.

    :param searchable: The search-term inputted by the end-user
    :type searchable: str or int
    :param wanted_note: any note that the end-user wants to put to a single buisness
    :type wanted_note: str
    :return: The updated business
    :rtype: dict
    """
    if type(searchable) == str and searchable.isdigit():
        searchable = int(searchable)
    business = db.find_one({"$or": [{"vat": searchable}, {"name": searchable}]})
    if business:
        business_id = business['_id']
        result = db.find_one_and_update(
            {"_id": business_id},
            {"$set":
                {"note": wanted_note}
             })
        return result
    else:
        raise ValueError("Business doesn't exist.")


def business_exists_in_db(searchable):
    """
    This function checks the DB for the existance of the business being passed as an argument

    :param searchable: An unique identifier for the business that need check for existence
    :type searchable: int or str
    :return: True or false
    :rtype: bool
    """
    if type(searchable) == str and searchable.isdigit():
        searchable = int(searchable)
    result = db.find_one({"$or": [{"vat": searchable}, {"name": searchable}]})
    if type(result) == dict:
        return True
    else:
        return False


def vat_to_coords(list_of_vat):
    """
    This function takes a list of VAT numbers and pulls the coordinates from the mongoDB and returns them as a list

    :param list_of_vat: takes a list with vat numbers in it
    :type list_of_vat: list
    :raises ValueError: raises an value error if no buisness with that VAT exists
    :return: list of coordinates from a single business
    :rtype: list
    """
    coords_list = []
    try:
        for x in list_of_vat:
            coord_set = f"{pull_single_business(x)['location'][0]}," \
                        f"{pull_single_business(x)['location'][1]}"
            coords_list.append(coord_set)
        return coords_list
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])
