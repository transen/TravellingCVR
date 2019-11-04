from cli_functions import *
import users

# TODO Go from if-sentences to loop-selection-states?

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
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    continue
                else:
                    break
            elif wanted_action == 3:
                break
            else:
                clear_interface()
                print("Not understood, try again.")
        else:
            cli_present_main_menu_options()
            try:
                wanted_action = int(input('Choose between 1-9: '))
            except ValueError:
                clear_interface()
                print("Please type a number.")
                continue
            if wanted_action == 1:
                cli_add_business()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 2:
                cli_pull_single_business()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 3:
                cli_pull_all_businesses()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 4:
                cli_delete_business()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 5:
                cli_change_status()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 6:
                cli_change_note()
                want_again = input("Want to do another operation? Y/N")
                if want_again == 'y' or want_again == 'Y':
                    clear_interface()
                    continue
                else:
                    break
            elif wanted_action == 7:
                cli_logout()
                continue
            elif wanted_action == 8:
                cli_delete_user()
            elif wanted_action == 9:
                break
            else:
                print("Not understood, try again.")


# executes if main.py is executed from CLI, but not if executed as a module during imports
if __name__ == "__main__":
    main()
