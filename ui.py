from pathlib import Path
import user as user_mod
from Profile import Profile, Post
from ds_client import send
import administration as admin
import ui as ui
import a4 as a4
import OpenWeather as WEA
import LastFM as LFM

server_adress = "168.235.86.101"
server_port = "3021"
administrator = False
temp_path = ''

def start():
    ui.administration(1)
    ui.command()


def user():
    global administrator
    user_type = input("Please input user type (\"admin\", \"user\"):  ")
    temp = 0
    if user_type == 'admin':
        temp = 1
        administrator = True
    else:
        temp = 0
        administrator = False
    return temp


def administration(a):
    global administrator
    if a == 1:
        administrator = True
    else:
        administrator = False
    return administrator


def command():
    command = input("please enter command:  ")
    command_type = command[0:1]
    if command == 'admin':
        admin.start()
    elif command == 'user':
        administrator == 0
        user()
        command()
    else:
        if command_type == "L":
            list_files_command(command)
        elif command_type == "Q":
            quit()
        elif command_type == "C":
            create_file(command)
            command()
        elif command_type == "D":
            del_file(command)
        elif command_type == "R":
            read_file(command)
        elif command_type == "H":
            user_mod.comm_list()
            command()
        elif command_type == "O":
            open_file(command)
            command()
        elif command_type == 'E':
            edit_file(command)
        elif command_type == "P":
            print_data(command)
        


def file_sort(a, b):
    temp = [f for f in a if Path(b, f).is_file()]
    return temp


def dir(pathlib_path, path):
    temp = []
    fol = Path(path)
    for item in fol.iterdir():
        if item.is_dir():
            temp.append(item)
    return temp


def list_files(a):
    if administrator:
        paths = a.split(' ')
        if len(paths) > 1:
            path = paths[1]
            recursive = "-r" in paths[2:]
            files_only = "-f" in paths[2:]
            search_file = None
            if "-s" in paths[2:]:
                s_index = paths.index("-s")
                if s_index + 1 < len(paths):
                    search_file = paths[s_index + 1]
            ending = None
            if "-e" in paths[2:]:
                e_index = paths.index("-e")
                if e_index + 1 < len(paths):
                    ending = paths[e_index + 1]
            list_items(path, recursive, files_only, search_file, ending)
        else:
            if administrator:
                print("please enter a valid path")
                command()
            else:
                user_mod.path_help()
    else:
        path = user_mod.get_path()
        recursive = user_mod.recursive()
        files_only = user_mod.files()
        ending = user_mod.ending()
        search_file = user_mod.search()
        print("OUTPUT:\n")
        list_items(path, recursive, files_only, search_file, ending)

def list_files_command(command):
    command_parts = command.split()
    paths = command_parts[1:]
    path = paths[0]
    recursive = "-r" in paths
    files_only = "-f" in paths
    search_file = None
    if "-s" in paths:
        s_index = paths.index("-s")
        if s_index + 1 < len(paths):
            search_file = paths[s_index + 1]
    ending = None
    if "-e" in paths:
        e_index = paths.index("-e")
        if e_index + 1 < len(paths):
            ending = paths[e_index + 1]
    list_items(path, recursive, files_only, search_file, ending)


def list_items(path, recursive=False, files_only=False, search_file=None, ending=None):
    try:
        l = Path(path).iterdir()
        
        files = file_sort(l, path)
        dirs = dir(l, path)

        for file in files:
            file_name, file_extension = file.stem, file.suffix
            file_extension = file_extension[1::]
            if search_file is None or search_file == file_name:
                if ending is None or file_extension.lower() == ending.lower():
                    print(file)

        if recursive:
            for directory in dirs:
                if not files_only and directory.is_dir():
                    if ending is not None:
                        list_items(directory, recursive, files_only, search_file, ending)
                    else:
                        print(directory)
                        list_items(directory, recursive, files_only, search_file, ending)
                elif files_only and directory.is_dir():
                    list_items(directory, recursive, files_only, search_file, ending)
        elif not files_only and ending is None:
            for directory in dirs:
                print(directory)
    except FileNotFoundError:
        print(f"the path {path} doesnt exist")
    command()


def create_file(a):
    global temp_path
    if administrator:
        paths = a.split(' ')
        if len(paths) > 1:
            path = paths[1]
            if '-n' in paths[2:]:
                n_index = paths.index('-n')
                temp = n_index + 1
                file_name = paths[temp]
                file_ext = file_name + '.dsu'
                filepath = Path(path) / file_ext
                username = None
                password = None
                bio = None
                profile = Profile(username = username, password = password, bio = bio)
                with open(filepath,'a') as f:
                    print("")
                f = open(filepath,'a')
                profile.save_profile(path = filepath)
                print(f'{filepath} OPENED')
                temp_path = filepath
        print(f"TEMP PATH:  {temp_path}")
        return temp_path        
    else:
        file_path = user_mod.get_path()
        file_name = user_mod.file_name()
        line = file_path + "\\" + file_name
        username = input("Enter Username:  ")
        password = input("Enter Password:  ")
        bio = input("Enter bio: ")
        profile = Profile(username = username, password = password, bio = bio)
        print(line + "      CREATED")
        with open(line, 'a') as f:
            a = "Username: " + username + '\n'
            f.write(a)
            b = "Password: " + password + '\n'
            f.write(b)
            c = "Bio: " + bio + '\n'
            f.write(c)
        profile.save_profile(path = line)
        f = open(line, 'a')
        temp_path = file_path
    print(f'{file_path} OPENED')
    print(f"this is the way  {file_path}")
    return temp_path


def check_file(a):
    if Path(a).exists():
        return True
    else:
        return False


def del_file(a):
    if administrator:
        paths = a.split(' ')
        path = paths[1]
        if path[-3:] == 'dsu':
            if check_file(path):
                Path(path).unlink()
                print(f"{path} DELETED")
            elif not check_file(path):
                print("no such file exists")
        else:
            print("can only delete dsu files")
    else:
        path = user_mod.get_path()
        if path[-3:] == 'dsu':
            if check_file(path):
                Path(path).unlink()
                print(f"{path} DELETED")
            elif not check_file(path):
                print("no file exists")
        else:
            print("can only delete dsu files")

    command()


def read_file(a):
    if administrator:
        paths = a.split(' ')
        path = paths[1]
        if path[-3:] == 'dsu':
            if check_file(path):
                with open(path, 'r') as p:
                    l = p.readlines()
                    if len(l) > 0:
                        for i in l:
                            print(i, end='')
                    else:
                        print("EMPTY")
            elif not check_file(path):
                print("no such file exists")
        print("")
    else:
        path = user_mod.get_path()
        if path[-3:] == 'dsu':
            if check_file(path):
                with open(path, 'r') as p:
                    l = p.readlines()
                    if len(l) > 0:
                        for i in l:
                            print(i, end='')
                    else:
                        print("EMPTY")
            elif not check_file(path):
                print("no file exists") 
        else:
            print("please enter a file with \".dsu\" extention")
    print("")
    command()


def open_file(a):
    global temp_path
    if administrator:
        path = a.split(' ')
        temp_path = path[1]
        f = open(temp_path, 'a')
        print(temp_path + " opened")
        return temp_path
    else:
        path = user_mod.get_path()
        print("Without the file extention,")
        name = user_mod.file_name()
        temp_path = path + "\\" + name
        f = open(temp_path, 'r+')
        print(temp_path + ' opened')
        for line in f:
            print(" ")
            print(line.strip())
    command()
    return temp_path
        

def edit_file(a):
    if administrator:
        lis = a.split(' ')
        bio_index = a.find('-bio')
        bio = ''
        if bio_index != -1:
            start_quote = a.find('"', bio_index)
            end_quote = a.find('"', start_quote + 1)
            if start_quote != -1 and end_quote != -1:
                bio = a[start_quote + 1:end_quote]
        
        profile = Profile()
        profile.load_profile(path = temp_path)
        
        if '-user' in lis:
            usr_index = lis.index('-user')
            new_usr = ' '.join(lis[usr_index + 1:]).strip('"')
            profile.username = new_usr
            profile.save_profile(temp_path)
        if '-addpost' in lis:
            post_index = lis.index('-addpost')
            post_content = ' '.join(lis[post_index + 1:])
            new_post = Post(post_content)
            profile.add_post(new_post)
            profile.save_profile(temp_path)
        if '-pwd' in lis:
            pwd_index = lis.index('-pwd')
            new_pwd= lis[pwd_index + 1]
            profile.password = new_pwd.strip('"')
            profile.save_profile(temp_path)
        if '-bio' in lis:
            profile.bio = bio.strip('"')
            profile.save_profile(temp_path)
    else:
        profile = Profile()
        print("please enter a dsu file path")
        temp_path = input()
        profile.load_profile(path = temp_path)
        print("what would you like to edit?")
        print("\"-user\" to update the username")
        print("\"-pwd\" to update password")
        print("\"-bio\" to update bio")
        print("\"-addpost\" to add a post")
        user_in = str(input())
        if "-user" in user_in:
            new = str(input("enter new username: "))
            profile.username = new
            profile.save_profile(temp_path)
        elif "-pwd" in user_in:
            new = str(input("enter new password: "))
            profile.password = new
            profile.save_profile(temp_path)
        elif "-bio" in user_in:
            new = str(input("enter new bio: "))
            profile.bio = new
            profile.save_profile(temp_path)
        elif "-addpost" in user_in:
            post_content = input("Enter new post: ")
            if "@W" in post_content or "@w" in post_content:
                zipc = input("Enter Zipcode: ")
                cc = input("Enter Country Code: ")
                Fire = WEA.OpenWeather(zipc, cc)
                Fire.set_apikey("ceb8cbc931c2f41301ba4a1548020fd4")
                Fire.load_data()
                post_content = Fire.transclude(post_content)   
            if "@L" in post_content or "@l" in post_content:
                alb = input("Enter Album Song Album: ")
                art = input("Enter Artist: ")
                Water = LFM.LastFM()
                Water.set_artist_album(art, alb)
                Water.setFMapi("7cd2ee13dc3b0100dae94c5c7401df50")
                Water.loadFMdata()
                #print(Water.loadFMdata())
                post_content = Water.transclude(post_content)
                
            new_post = Post(post_content)
            profile.add_post(new_post)
            profile.save_profile(temp_path)
            temp = input("would you like to post this on a server?  Y/N:    ")
            if temp == "Y":
                serv = input("please input a server:   ")
                port = 3021
                username = profile.username
                password = profile.password
                message = post_content
                send(serv, port, username, password, message)

    command()


def print_data(command):
    global temp_path
    
    options = command.split()[1:]

    profile = Profile()
    profile.load_profile(temp_path)

    if '-usr' in options:
        print("Username:", profile.username)
    if '-pwd' in options:
        print("Password:", profile.password)
    if '-bio' in options:
        print("Bio:", profile.bio)
    if '-posts' in options:
        for i, post in enumerate(profile._posts):
            print(f"Post {i}: {post}")
    if '-post' in options:
        post_index = options.index('-post')
        post_id = int(options[post_index + 1])
        if 0 <= post_id < len(profile._posts):
            print(f"Post {post_id}: {profile._posts[post_id]}")
        else:
            print("Invalid post ID")
    if '-all' in options:
        print("Username:", profile.username)
        print("Password:", profile.password)
        print("Bio:", profile.bio)
        print("Posts:")
        for i, post in enumerate(profile._posts):
            print(f"  Post {i}: {post}")
    command()

if __name__ == "__main__":
    start()   

