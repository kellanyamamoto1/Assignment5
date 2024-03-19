from pathlib import Path
import administration as admin
import ui as ui


command_list = """
L -- List all files in a specified path
Q -- Quit the program entirely
C -- Create a new file in a specified path
D -- Deleted a file
R -- Read a file
O -- Open a file
Help -- Relist commands
"""


def comm_list():
    print(command_list)

def start():
    ui.administration(0)
    ui.command()
    

def path_help():
    print("Please enter a valid path in the form:")
    print("[COMMAND] [PATH] [[-]OPTION] [INPUT]")
    print("If you need to view all commands, enter \"Help\"")
    ui.command()


def get_path():
    print("Please enter a path:")
    path = input()
    return path

def files():
    print("would you like to only display files? Y/N")
    temp = input()
    if temp == "Y":
        file = True
    else:
        file = False
    return file

def recursive():
    print("would you like to search recursively? Y/N")
    re = input()
    if re == "Y":
        recursive = True
    else:
        recursive = False
    return recursive

def ending():
    print("would you like to search for a specific file type? Y/N")
    temp = input()
    if temp == 'Y':
        ending = input("please enter file extention (without a period, ie: txt, jpg, dsu):\n")
        return ending
    else:
        return None

def file_name():
    print("got here")
    name = input("Please enter a file name:  ")
    name = name + ".dsu"
    return name

def search():
    print("Would you like to search for a specific file? Y/N")
    temp = input()
    if temp == 'Y':
        name = input("Please enter the file you would like to search for:\n")
        return name
    else:
        return None
