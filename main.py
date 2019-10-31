import getpass
from cvrapi import *
from mongofunctions import *
from users import *
from prettytable import PrettyTable
from cli_functions import *

logged_in_user = None




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
    # Testing of pull_single_business
    try:
        print(pull_single_business(testarg))
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])
        return None  # breaks function


# test("38158686")


while True:
    """The infinite loop initiated to perform the CLI-portion"""
    if not logged_in_user:
        clear_interface()
        """Prompts a user to log in"""
        print('Welcome! Please either log in, or create a user if you don\'t have one already')
        print('1: Log in')
        print('2: Create user')
        try:
            wanted_action = int(input('Choose between 1-2: '))
        except ValueError:
            clear_interface()
            print("Please type a number.")
            continue
        if wanted_action == 1:
            clear_interface()
            try_username = input("Username: ")
            try_password = getpass.getpass()
            try:
                result = login(try_username, try_password)
                logged_in_user = result
            except ValueError as err:
                print("Login error: " + err.args[0])
                continue
        elif wanted_action == 2:
            clear_interface()
            cli_add_user()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        else:
            clear_interface()
            print("Not understood, try again.")
    else:
        clear_interface()
        print(f"Welcome back {logged_in_user['username']}!")
        print('What action would you like to perform?')
        print('1: Add a new business')
        print('2: Show a single business')
        print('3: Show all businesses')
        print('4: Delete a business')
        print('5: Change status of a business')
        print('6: Change note of a business')
        print('7: Log out')
        print('8: Delete user')
        print('9: End program')
        try:
            wanted_action = int(input('Choose between 1-9: '))
        except ValueError:
            clear_interface()
            print("Please type a number.")
            continue
        if wanted_action == 1:
            clear_interface()
            business = input("Input name or VAT of business to be added: ")
            cli_add_business(business)
            print("Business added!")
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 2:
            clear_interface()
            cli_pull_single_business()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 3:
            clear_interface()
            cli_pull_all_businesses()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 4:
            clear_interface()
            cli_delete_business()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 5:
            clear_interface()
            cli_change_status()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 6:
            clear_interface()
            cli_change_note()
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 7:
            clear_interface()
            logout()  # Doesn't do anything atm... A problem with altering variables from modules?
            logged_in_user = None
            continue
        elif wanted_action == 8:
            clear_interface()
            certain = input(f"Are you sure you want to delete user '{logged_in_user['username']}'? y/n:")
            if certain == "y" or certain == "Y":
                delete_user(logged_in_user["username"])
                print(f"User '{logged_in_user['username']}' deleted!")
                logout()
                logged_in_user = None
                break
        elif wanted_action == 9:
            break
        else:
            print("Not understood, try again.")
