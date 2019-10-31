import subprocess
import getpass
from cvrapi import *
from mapquestapi import *
from mongofunctions import *
from prettytable import PrettyTable
from users import *


# Clears the terminal-window
def clear_interface():
    subprocess.call('clear', shell=True)


def cli_add_business(business):
    # attempt to grab a business
    try:
        business = business_from_api(business)
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
        result = insert_business(business)
        print(f"'{result['name']}' succesfully inserted!'")
    except ValueError as err:
        print("INSERT ERROR: " + err.args[0])
        return None  # breaks function


def cli_pull_single_business():
    business = input("Input name or VAT of business you want to find: ")
    try:
        business = pull_single_business(business)
        t = PrettyTable(["Key", "Value"])
        for key in business:
            t.add_row([key, business[key]])
        print(t)
    except ValueError as err:
        print("PULL ERROR: " + err.args[0])


def cli_pull_all_businesses():
    print('You can sort the businesses by either [name] [zipcode] [vat] [status].')
    sorting = input("How would you like to sort the businesses? ")
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


def cli_delete_business():
    business = input("Input name or VAT of business you want to delete: ")
    try:
        delete_business(business)
        print('Deleted business')
    except ValueError as err:
        print(f'Business didn\'t exist: "{err.args[0]}"')


def cli_add_user():
    chosen_username = input("Input username: ")
    chosen_email = input("Input email: ")
    chosen_password = getpass.getpass()
    chosen_address = input("Input address: ")
    try:
        add_user(chosen_username, chosen_email, chosen_password, chosen_address)
    except ValueError as err:
        print("ERROR", err.args[0])


def cli_change_status():
    business = input("Name or VAT of business you want to change status of: ")
    status = int(input("New status for business (1-5): "))
    try:
        result = change_status(business, status)
        print(f"Status of '{result['name']}' changed to '{result['status']}'!")
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])


def cli_change_note():
    business = input("Name or VAT of business you want to change status of: ")
    note = input("New note for business: ")
    try:
        result = change_note(business, note)
        print(f"Note for '{result['name']}' changed from '{result['note']} to '{note}'")
    except ValueError as err:
        print("STATUS-CHANGE ERROR: " + err.args[0])


def cli_present_options():
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
