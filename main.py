from mongofunctions import *
from cvrapi import *
from mapquestapi import *
from users import *
import getpass


def test(testarg):
    """
    A function solely to test code written so far, will change over time
    """
    # deletes the business in mongodb if it exists
    try:
        delete_business(testarg)
        print('Deleted business')
    except ValueError as err:
        print(f'Business didn\'t exist: "{err.args[0]}"')
    # attempt to grab a business
    try:
        business = business_from_api(testarg)
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        return None  # breaks function
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        return None  # breaks function
    # attempt to insert the business to mongodb
    try:
        insert_business(business)
        # return business  # to end function
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return None  # breaks function
    # Testing of pull_single_business
    try:
        print(pull_single_business(testarg))
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])
        return None  # breaks function


# test("38158686")



while True:
    """The infinite loop initiated to perform the CLI-portion"""
    print('What action would you like to perform?')
    print('1: Add user')
    print('2: Log in')
    wanted_action = int(input('Choose between 1-2: '))
    if wanted_action == 1:
        chosen_username = input("Input username: ")
        chosen_email = input("Input email: ")
        chosen_password = getpass.getpass()
        chosen_address = input("Input address: ")
        isAdmin = False  # needed?
        try:
            add_user(chosen_username, chosen_email, chosen_password, chosen_address, isAdmin)
        except ValueError as err:
            print("ERROR", err.args[0])
        want_again = input("Want to do another operation? Y/N")
        if want_again == 'y' or want_again == 'Y':
            continue
        else:
            break
    elif wanted_action == 2:
        try_username = input("Input username: ")
        try_password = getpass.getpass()
        login(try_username, try_password)
        want_again = input("Want to do another operation? Y/N")
        if want_again == 'y' or want_again == 'Y':
            continue
        else:
            break
    else:
        print("Not understood, try again.")
