import subprocess
import getpass

from api_helpers.mapquestapi import *
from db_helper.mongofunctions import *
from prettytable import PrettyTable
from user_helpers import users
import cli_main
from user_helpers.users import update_user_last_login


# Clears the terminal-window
def clear_interface():
    subprocess.call('clear', shell=True)


def cli_add_business():
    clear_interface()
    business = input("Input name or VAT of business to be added: ")  # TODO check input for valid 8-digit if only digits
    # attempt to grab a business
    try:
        business = business_from_api(business)
        if business["protected"]:
            print("This business is protected against contacting them for ad-purposes.")
            sure = input("Are you sure you want to add them to the database? Y/N ")
            if sure == "n" or sure == "N":
                print(f"'{business['name']}' not added because of protected-status")
                return None
    except ValueError as err:
        print("API ERROR: " + err.args[0])
        cli_return_to_main_menu()
        return None  # breaks function
    # attempt to fetch coordinates
    try:
        business = attach_coords(business)
    except ValueError as err:
        print("COORDS ERROR: " + err.args[0])
        cli_return_to_main_menu()
        return None  # breaks function
    # attempt to insert the business to mongodb
    try:
        result = insert_business(business)
        print(f"'{result['name']}' succesfully inserted!")
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return None  # breaks function
    cli_return_to_main_menu()


def cli_pull_single_business():
    clear_interface()
    business = input("Input name or VAT of business you want to find: ")
    try:
        business = pull_single_business(business)
        t = PrettyTable(["Key", "Value"])
        for key in business:
            t.add_row([key, business[key]])
        print(t)
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])
    cli_return_to_main_menu()


def cli_pull_all_businesses():
    clear_interface()
    print('You can sort the businesses by either [name] [zipcode] [vat] [status]. Default is name.')
    sorting = input("How would you like to sort the businesses? ")
    if sorting == "":
        sorting = "name"
    clear_interface()
    try:
        businesses = pull_all_businesses(sorting)
        t = PrettyTable(['Name', 'VAT', 'Zipcode', 'Status', 'Note', 'Map URL'])
        for business in businesses:
            t.add_row([business['name'], business['vat'], business['zipcode'], business['status'],
                       business['note'], business['map url']])
        print(t)
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])
    cli_return_to_main_menu()


def cli_delete_business():
    clear_interface()
    business = input("Input name or VAT of business you want to delete: ")
    try:
        delete_business(business)
        print('Deleted business')
    except ValueError as err:
        print(f'Business didn\'t exist: "{err.args[0]}"')
    cli_return_to_main_menu()


def cli_add_user():
    clear_interface()
    chosen_username = input("Input username: ")
    chosen_email = input("Input email: ")
    chosen_password = getpass.getpass()
    chosen_address = input("Input address (Format: <streetname> <housenumber>, <zipcode> <city>, <countrycode>):\n")
    try:
        users.add_user(chosen_username, chosen_email, chosen_password, chosen_address)
        print("User created successfully!")
    except ValueError as err:
        print("ERROR", err.args[0])
    cli_return_to_main_menu()


def cli_change_status():
    clear_interface()
    business = input("Name or VAT of business you want to change status of: ")
    status = int(input("New status for business (1-5): "))
    try:
        result = change_status(business, status)
        print(f"Status of '{result['name']}' changed to '{result['status']}'!")
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])
    cli_return_to_main_menu()


def cli_change_note():
    clear_interface()
    business = input("Name or VAT of business you want to change status of: ")
    note = input("New note for business: ")
    try:
        result = change_note(business, note)
        print(f"Note for '{result['name']}' changed from '{result['note']}' to '{note}'")
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])
    cli_return_to_main_menu()


def cli_present_login_menu_options():
    print('1: Log in')
    print('2: Create user')
    print('3: Exit program')


def cli_present_main_menu_options():
    print('What action would you like to perform?')
    print('1: Add a new business')
    print('2: Show a single business')
    print('3: Show all businesses')
    print('4: Delete a business')
    print('5: Change status of a business')
    print('6: Change note of a business')
    print('7: Log out')
    print('8: Delete user')
    print('9: Add a business to your current selection')
    print('10: Show your current selection')
    print('0: End program')


def cli_login():
    clear_interface()
    try_username = input("Username: ")
    try_password = getpass.getpass()
    try:
        result = users.login(try_username, try_password)
        users.logged_in_user = result
        clear_interface()
        update_user_last_login(try_username)
        print(f"Welcome back {users.logged_in_user['username']}!")
    except ValueError as err:
        clear_interface()
        print("Login error: " + err.args[0])


def cli_logout():
    clear_interface()
    users.logout()


def cli_delete_user():
    clear_interface()
    certain = input(f"Are you sure you want to delete user '{users.logged_in_user['username']}'? y/n:")
    if certain == "y" or certain == "Y":
        users.delete_user(users.logged_in_user["username"])
        print(f"User '{users.logged_in_user['username']}' deleted!")
        users.logout()


def cli_save_to_selection():  # TODO IMPLEMENT
    clear_interface()
    business_to_add = input("Enter VAT: ")
    if business_exists_in_db(business_to_add):
        cli_main.current_selection.append(business_to_add)
        print(f"{business_to_add} added to selection!")
    else:
        print("Business doesn't exist in db. Try again!")
    cli_return_to_main_menu()


def cli_show_selection():  # TODO IMPLEMENT
    clear_interface()
    print("Your current selection:")
    print(*cli_main.current_selection)
    cli_return_to_main_menu()


def cli_return_to_main_menu():
    input("Press [ENTER] to continue to main menu")
    clear_interface()
