from cli_helpers.cli_functions import *
from user_helpers import users

current_selection = []


def main():
    clear_interface()
    print('Welcome! Please either log in, or create a user if you don\'t have one already.')
    while True:
        """The infinite loop initiated to perform the CLI-portion"""
        if not users.logged_in_user:
            """Prompts a user to log in"""
            cli_present_login_menu_options()
            try:
                wanted_action = int(input('Choose between 1-3: '))
            except ValueError:
                clear_interface()
                print("Please type a number.")
                continue
            if wanted_action == 1:
                cli_login()
            elif wanted_action == 2:
                cli_add_user()
            elif wanted_action == 3:
                break
            else:
                clear_interface()
                print("Not understood, did you write a single number between 1 and 3?.")
        else:
            cli_present_main_menu_options()
            try:
                wanted_action = int(input('Choose between 1-10: '))
            except ValueError:
                clear_interface()
                print("Please type a number.")
                continue
            if wanted_action == 1:
                cli_add_business()
            elif wanted_action == 2:
                cli_pull_single_business()
            elif wanted_action == 3:
                cli_pull_all_businesses()
            elif wanted_action == 4:
                cli_delete_business()
            elif wanted_action == 5:
                cli_change_status()
            elif wanted_action == 6:
                cli_change_note()
            elif wanted_action == 7:
                cli_logout()
                continue  # back to login-menu
            elif wanted_action == 8:
                cli_delete_user()
            elif wanted_action == 9:
                cli_save_to_selection()
            elif wanted_action == 10:
                cli_show_selection()
            elif wanted_action == 0:
                break
            else:
                print("Not understood, did you write a number between 1 and 10?.")


# executes if cli_main.py is executed from CLI, but not if executed as a module during imports
if __name__ == "__main__":
    main()
