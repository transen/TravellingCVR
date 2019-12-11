from api_helpers.mapquestapi import *
from db_helpers.mongofunctions import *
from user_helpers import users
from user_helpers.password_hashing import verify_password
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
        raise ValueError("Business doesn't exist.")  # breaks function and bubbles error to front-end
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
    This function is able to change the status shown on the frontend by calling the change_status()
    function. If an error is caught changing the status it reraises the valueError and prints an error message.

    :param business: A name or VAT number of a buisness
    :type business: str or int
    :param new_status: the new status that replaces an old or non-existiting one
    :raises: ValueError, if the status is not a number between 1-5
    :return: new dictionary with the updated status
    :rtype: dict
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
    
    This function is made for changing the note that appears in the database and front-end
    the function works by invoking one of our mongofunctions so it takes the DB entry called notes
    and updates it to whatever the user enters

    :param business: a name or VAT of a buisness
    :type business: str or int
    :param new_note: the note that the user wants to appear on the site
    :type new_note: str
    :raises: ValueError, if an error occurs in the change_note function it's raised to the front-end
    :return: the buisness with the updated note
    :rtype: dict
    """
    try:
        result = change_note(business, new_note)
        print(f"Note for '{result['name']}' changed from '{result['note']}' to '{new_note}'")
        return result
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])
        raise ValueError(err.args[0])


def app_create_user(username, email, password, address):
    """
    This function attempts to add a user to the database (see documentation for user_helpers.users.add_user()).
    If successful, a confirmation-message will be printed to the console, and the username will be returned for handling
    in the front-end. If an error occurs, a ValueError will be raised for handling in the front-end.

    :param username: The chosen username
    :type username: str
    :param email: The chosen email
    :type email: str
    :param password: The chosen password
    :type password: str
    :param address: The chosen address
    :type address: str
    :return: The username of the newly created user
    :rtype: str
    """
    try:
        users.add_user(username, email, password, address)
        print(f'User "{username}" created successfully!')
        return username
    except ValueError as err:
        raise ValueError(err.args[0])


def app_delete_user(username):
    """
    This function lets the user delete the user from the front end, it's enabled by calling the delete_user()
    function from db_helpers/mongofunctions.py

    :param username: the username of the active user
    :type username: str
    :raises: ValueError, if an error occurs it's caught and displays it as an error message instead of crashing the system
    :return: returns the string to the delete_user() function in mongofunctions.py
    :rtype: str
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
    This function is for creating a route from a list of coordinates from buisnesses chosen by the user
    it works by taking a list of coordinates using the list_to_coords() function, aftewards
    it checks the coordinates connected to the username of the active user and appends them to the list
    which is going to be the final optimized route. By calling optimized_order() and 
    create_optimized_url() by using the location sequence in the returned mapquest json we're able to
    construct the google maps URL.

    :param list_of_vat: a list of VAT numbers
    :type list_of_vat: list
    :param username: the username of the current user
    :type username: str
    :raises: ValueError, if any errors occur during the process it displays an error message instead of crashing
    :return: the optimized route in google maps in the form of a URL
    :rtype: str
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
