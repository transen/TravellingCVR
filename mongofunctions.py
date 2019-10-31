from pymongo import MongoClient, ReturnDocument
from pymongo.errors import DuplicateKeyError
from config import *
from mapquestapi import *
from cvrapi import *

# MongoDB initial setup
db = MongoClient(mongoclientstring).travellingcvr.businesses  # mongoclientstring hidden in config.py


def insert_business(business):
    """
    This function inserts a business into the mongodb, via the module "Pymongo" which bridges the gap between python and
    and the hosted MongoDB-database. MongoDB is inherently noSQL, compared to a traditional relational SQL-database,
    which we are accustomed to, and used to work with. This has been an intentionally added challenge, in order to
    obtain more practical knowledge of noSQL-moddeled behaviour in regards to non-structured data.
    TODO explain this further

    :param business:
    :type business:
    :raises ValueError:
    :return:
    :rtype:
    """
    try:
        db.insert_one(business)
        return business
    except DuplicateKeyError:
        raise ValueError(f'A business with the VAT \'{business["vat"]}\' already exists!')


def pull_single_business(searchable):
    """
    Pulls a single business from MongoDB from VAT-parameter or name of business
    TODO explain this further
    TODO make the entire business searchable. Good idea? Just name and VAT?

    :param searchable:
    :type searchable:
    :raises ValueError:
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

    TODO expand this

    :param sorted_by:
    :type sorted_by:
    :return: A list of all businesses located in the database.
    :rtype: list
    """

    result = list(db.find({}).sort(sorted_by, 1))
    if type(result) == list:
        output = []
        for business in result:
            # output.append({'name': business['name'], 'vat': business['vat']})
            output.append(business)
        # for business in output:
        #     print(f"{business['name']}\t{business['vat']}")
        return output
    else:
        raise ValueError("Something went wrong")


def delete_business(searchable):
    """
    This function aims to delete a business from the MongoDB, if it exists. It starts off checking whether the queried
    business exists in the DB. If 'result' returns a dictionary, the business exists, and utilizes the built-in pymongo
    "delete_one"-method to delete the business-document from the DB. The function then returns the deleted business,
    for further handling and presentation to the end-user.

    TODO Perhaps make it a regex to achieve partial match - is that even what we want?

    :param searchable:
    :type searchable:
    :raises ValueError:
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


def change_status(searchable, wanted_status):
    """
    This function changes the status of a business in the mongodb.

    :param searchable:
    :type searchable: str or int
    :param wanted_status:
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

    :param searchable:
    :type searchable: str or int
    :param wanted_note:
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
