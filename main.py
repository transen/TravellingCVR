import getpass
from cvrapi import *
from mongofunctions import *
from users import *
from prettytable import PrettyTable

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
        """Prompts a user to log in"""
        print('Welcome! Please either log in, or create a user if you don\'t have one already')
        print('1: Log in')
        print('2: Create user')
        wanted_action = int(input('Choose between 1-2: '))
        if wanted_action == 1:
            try_username = input("Input username: ")
            try_password = getpass.getpass()
            try:
                result = login(try_username, try_password)
                logged_in_user = result
            except ValueError as err:
                print("Login error: " + err.args[0])
                continue
        elif wanted_action == 2:
            chosen_username = input("Input username: ")
            chosen_email = input("Input email: ")
            chosen_password = getpass.getpass()
            chosen_address = input("Input address: ")
            try:
                add_user(chosen_username, chosen_email, chosen_password, chosen_address)
            except ValueError as err:
                print("ERROR", err.args[0])
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        else:
            print("Not understood, try again.")
    else:
        print(f"Welcome back {logged_in_user['username']}!")
        print('What action would you like to perform?')
        print('1: Add a new business')
        print('2: Show a single business')
        print('3: Show all businesses')
        print('4: Delete a business')
        print('5: Log out')
        print('6: Delete user')
        print('7: End program')
        wanted_action = int(input('Choose between 1-6: '))
        if wanted_action == 1:
            business = input("Input name or VAT of business to be added: ")
            add_business(business)
            print("Business added!")
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 2:
            business = input("Input name or VAT of business you want to find: ")
            try:
                business = pull_single_business(business)
                t = PrettyTable(["Key", "Value"])
                for key in business:
                    t.add_row([key, business[key]])
                print(t)
            except ValueError as err:
                print("PULL ERROR: " + err.args[0])
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 3:
            print('You can sort the businesses by either [name] [zipcode] [vat]. Default is [name].')
            sorting = input("How would you like to sort the businesses? ")
            if sorting is not "":
                try:
                    businesses = pull_all_businesses(sorting)
                    t = PrettyTable(['Name', 'VAT', 'Zipcode'])
                    for business in businesses:
                        t.add_row([business['name'], business['vat'], business['zipcode']])
                    print(t)
                except ValueError as err:
                    print("PULL ERROR: " + err.args[0])
            else:
                businesses = pull_all_businesses()
                for business in businesses:
                    print(f"{business['name']}\t{business['vat']}")  # TODO use pprint?
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 4:
            business = input("Input name or VAT of business you want to delete: ")
            try:
                delete_business(business)
                print('Deleted business')
            except ValueError as err:
                print(f'Business didn\'t exist: "{err.args[0]}"')
            want_again = input("Want to do another operation? Y/N")
            if want_again == 'y' or want_again == 'Y':
                continue
            else:
                break
        elif wanted_action == 5:
            logout()  # Doesn't do anything atm... A problem with altering variables from modules?
            logged_in_user = None
            continue
        elif wanted_action == 6:
            certain = input(f"Are you sure you want to delete user '{logged_in_user['name']}'? y/n:")
            if certain == "y" or certain == "Y":
                delete_user(logged_in_user["username"])
                print(f"User '{logged_in_user['username']}' deleted!")
                logout()
                logged_in_user = None
                break
        elif wanted_action == 7:
            break
        else:
            print("Not understood, try again.")
