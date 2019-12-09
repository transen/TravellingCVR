from api_helpers.mapquestapi import *
from db_helper.mongofunctions import *
from user_helpers import users
from user_helpers.users import pull_user


def app_add_business(business):
    """
    This function runs through the steps of adding a new business to the database. It starts out pulling the business
    from an API (see documentation for business_from_api()), it then fetches and attaches coordinates (see documentation
    for attach_coords()), then attempts to insert the business into the database. If successfull throughout, it will
    return the business in the form of a dictionary for use in the front-end. If any ValueErrors are raised in the
    function-chain, the function will except it, break, and reraise it for handling in the frontend, after the error is
    printed to the console.

    :param business: a name or VAT-number of a business
    :type business: str or int
    :raises: ValueError, raises if something is caught in the intermediary functions.
    :return: the business
    :rtype: dict
    """
    try:
        business = business_from_api(business)
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        #: breaks function and bubbles error to front-end
        raise ValueError("Business doesn't exist.")
    # Attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        #: Breaks function and bubbles error to front-end
        raise ValueError("The businesses' address couldn't be determined")
    # Attempt to insert the business to database
    try:
        business = insert_business(business)
        print(f"'{business['name']}' succesfully inserted!")
        return business
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        #: Breaks function and bubbles error to front-end
        raise ValueError("That business already exists in the system!")


def app_change_status(business, new_status):
    """

    :param business:
    :type business:
    :param new_status:
    :raises: ValueError,
    :return:
    :rtype:
    """
    try:
        new_status = int(new_status)
        try:
            result = change_status(business, new_status)
            print(f"Status of '{result['name']}' changed to '{result['status']}'!")
            return result
        except ValueError as err:
            print("STATUS-CHANGE ERROR: " + err.args[0])
            raise ValueError(err.args[0])
    except ValueError:
        raise ValueError("Status can only be a number between 1-5")


def app_change_note(business, new_note):
    """


    :param business:
    :type business:
    :param new_note:
    :type new_note:
    :raises: ValueError,
    :return:
    :rtype:
    """
    try:
        result = change_note(business, new_note)
        print(f"Note for '{result['name']}' changed from '{result['note']}' to '{new_note}'")
        return result
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])
        raise ValueError(err.args[0])


def app_create_user(username, email, password, address):
    try:
        users.add_user(username, email, password, address)
        print(f'User "{username}" created successfully!')
        return username
    except ValueError as err:
        raise ValueError(err.args[0])


def app_delete_user(username):
    """


    :param username:
    :type username:
    :raises: ValueError,
    :return:
    :rtype:
    """
    try:
        users.delete_user(username)
        print(f"User '{username}' deleted!")
        return username
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])


def app_create_optimized_route(list_of_vat, username):
    """


    :param list_of_vat:
    :type list_of_vat:
    :param username:
    :type username:
    :raises:
    :return:
    :rtype:
    """
    try:
        list_of_coords = vat_to_coords(list_of_vat)
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])
    try:
        user_coords = f"{pull_user(username)['location'][0]},{pull_user(username)['location'][1]}"
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])

    list_of_coords.insert(0, user_coords)
    list_of_coords.append(user_coords)

    try:
        optimized_list = optimize_order(list_of_coords)
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])
    try:
        optimized_url = create_optimized_url(optimized_list)
        return optimized_url
    except ValueError as err:
        print(err.args[0])
        raise ValueError(err.args[0])
