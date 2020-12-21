import os

def main():
    print_welcome_message()
    mode = select_mode()
    execute_mode(mode)

def select_mode(retry = False):

    if(retry):
        os.system('cls')

    print("To start the program you need to select one of the following options:")
    print("A: wizard")
    print("B: config file")
    print("C: about")
    print("X: exit")
    print()
    if(retry):
        print("That was not a valid option. Please try again.")
    mode = input("Option: ")

    possible_options = ["A", "B", "C", "X"]

    if (mode.upper() not in possible_options):
        select_mode(True)

    return mode.upper()

def execute_mode(mode):
    if (mode == "A"):
        wizard_mode()
    elif (mode == "B"):
        config_mode()
    elif (mode == "C"):
        about_mode()
    else:
        exit()

def wizard_mode():
    pass

def config_mode():
    pass

def about_mode():
    os.system('cls')
    print("About this tool:")
    print()
    print("This tool is created by the group named: \"Parkeerplaats speurders\".")
    print("It was created in a school project for the company TheRightDirection.")
    print("")
    answer = input("Do you want to return to the main menu? Y/n ")

    if(answer.upper() == "Y" or answer == ""):
        os.system('cls')
        mode = select_mode()
        execute_mode(mode)
    else:
        exit()

def exit():
    print("Good bye")

def print_welcome_message():
    os.system('cls')
    print("Welcome to AIDA: Aerial Imagery Downloader and Analyzer")
    print("With this tool you can download and analyze Areial Imaergy automaticly.")
    print()

main()